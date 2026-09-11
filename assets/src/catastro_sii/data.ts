/** Public aggregate JSON only. Memory belongs to this page/build; nothing is
 * persisted in localStorage, IndexedDB or a service worker. Mutable URLs are
 * revalidated through HTTP after five minutes, not forced stale indefinitely. */
type CacheOptions = {
  fetcher?: typeof fetch;
  now?: () => number;
  ttlMs?: number;
  maxEntries?: number;
  maxEstimatedBytes?: number;
};

type Entry = { promise: Promise<unknown>; expires: number; estimatedBytes: number };

export class JsonResourceCache {
  private readonly entries = new Map<string, Entry>();
  private readonly options: Required<CacheOptions>;

  constructor(options: CacheOptions = {}) {
    this.options = {
      fetcher: (...args) => fetch(...args), now: Date.now,
      ttlMs: 5 * 60_000, maxEntries: 16, maxEstimatedBytes: 8 * 1024 * 1024,
      ...options
    };
  }

  get<T>(url: string): Promise<T> {
    const existing = this.entries.get(url);
    if (existing && existing.expires > this.options.now()) {
      this.entries.delete(url);
      this.entries.set(url, existing);
      return existing.promise as Promise<T>;
    }
    this.entries.delete(url);
    const entry: Entry = { promise: Promise.resolve(), expires: Infinity, estimatedBytes: 0 };
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15_000);
    entry.promise = this.options.fetcher(url, { cache: "no-cache", signal: controller.signal })
      .then(async (response) => {
        if (!response.ok) throw new Error(`${url} respondió ${response.status}`);
        const payload = await response.json();
        // Conservative serialized payload estimate; it is not a JS heap limit.
        entry.estimatedBytes = JSON.stringify(payload).length * 2;
        entry.expires = this.options.now() + this.options.ttlMs;
        this.trim();
        return payload;
      })
      .catch((error: unknown) => {
        if (this.entries.get(url) === entry) this.entries.delete(url);
        throw error;
      })
      .finally(() => clearTimeout(timeout));
    this.entries.set(url, entry);
    this.trim();
    return entry.promise as Promise<T>;
  }

  private trim(): void {
    let bytes = [...this.entries.values()].reduce((sum, entry) => sum + entry.estimatedBytes, 0);
    while (this.entries.size > this.options.maxEntries || bytes > this.options.maxEstimatedBytes) {
      const oldest = this.entries.keys().next().value;
      if (oldest === undefined) break;
      bytes -= this.entries.get(oldest)?.estimatedBytes ?? 0;
      this.entries.delete(oldest);
    }
  }
}

const resources = new JsonResourceCache();
export function jsonResource<T>(url: string): Promise<T> { return resources.get<T>(url); }

declare global {
  interface Window { catastroCommuneRows?: Promise<unknown>; }
}

/** Reuse the legacy selector's current-page request, including while in flight. */
export async function communeRows<T>(url: string): Promise<T> {
  if (typeof window !== "undefined" && window.catastroCommuneRows) {
    try { return await window.catastroCommuneRows as T; }
    catch { delete window.catastroCommuneRows; }
  }
  return jsonResource<T>(url);
}
