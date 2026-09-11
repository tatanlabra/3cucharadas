import { afterEach, describe, expect, it, vi } from "vitest";
import { communeRows, JsonResourceCache } from "../../assets/src/catastro_sii/data";

afterEach(() => { vi.unstubAllGlobals(); vi.useRealTimers(); });

describe("caché JSON acotada por página", () => {
  it("comparte petición y parseo concurrentes y conserva la versión de la URL", async () => {
    const fetcher = vi.fn<typeof fetch>(async () => new Response('{"features":[]}'));
    const cache = new JsonResourceCache({ fetcher });
    const [first, second] = await Promise.all([cache.get("https://local/uv?v=1"), cache.get("https://local/uv?v=1")]);
    expect(first).toBe(second);
    await cache.get("https://local/uv?v=2");
    expect(fetcher).toHaveBeenCalledTimes(2);
    expect(fetcher.mock.calls[0]?.[1]?.cache).toBe("no-cache");
  });

  it("un fallo HTTP o JSON no envenena el reintento", async () => {
    const fetcher = vi.fn()
      .mockResolvedValueOnce(new Response("fallo", { status: 503 }))
      .mockResolvedValueOnce(new Response("no es JSON"))
      .mockResolvedValueOnce(new Response('{"ok":true}'));
    const cache = new JsonResourceCache({ fetcher });
    await expect(cache.get("/dato")).rejects.toThrow("503");
    await expect(cache.get("/dato")).rejects.toThrow();
    await expect(cache.get("/dato")).resolves.toEqual({ ok: true });
    expect(fetcher).toHaveBeenCalledTimes(3);
  });

  it("revalida tras TTL y expulsa el dato menos utilizado", async () => {
    let now = 0;
    const fetcher = vi.fn(async () => new Response('{"ok":true}'));
    const cache = new JsonResourceCache({ fetcher, now: () => now, ttlMs: 100, maxEntries: 2 });
    await cache.get("/a");
    await cache.get("/b");
    await cache.get("/a");
    await cache.get("/c");
    await cache.get("/b");
    expect(fetcher).toHaveBeenCalledTimes(4);
    now = 101;
    await cache.get("/b");
    expect(fetcher).toHaveBeenCalledTimes(5);
  });

  it("no retiene recursos mayores que el presupuesto", async () => {
    const fetcher = vi.fn(async () => new Response('{"large":"123456789"}'));
    const cache = new JsonResourceCache({ fetcher, maxEstimatedBytes: 8 });
    await cache.get("/large");
    await cache.get("/large");
    expect(fetcher).toHaveBeenCalledTimes(2);
  });

  it("usa las filas del selector existente sin segunda descarga", async () => {
    const rows = [{ codigo_comuna: "13101" }];
    vi.stubGlobal("window", { catastroCommuneRows: Promise.resolve(rows) });
    const fetcher = vi.fn();
    vi.stubGlobal("fetch", fetcher);
    expect(await communeRows("/comunas")).toBe(rows);
    expect(fetcher).not.toHaveBeenCalled();
  });

  it("reintenta si falló la petición compartida del selector", async () => {
    vi.stubGlobal("window", { catastroCommuneRows: Promise.reject(new Error("offline")) });
    vi.stubGlobal("fetch", vi.fn(async () => new Response("[]")));
    await expect(communeRows("/comunas-retry")).resolves.toEqual([]);
    expect(window.catastroCommuneRows).toBeUndefined();
  });

  it("aborta una petición colgada y libera la entrada para reintentar", async () => {
    vi.useFakeTimers();
    const fetcher = vi.fn<typeof fetch>().mockImplementationOnce((_url, options) => new Promise((_resolve, reject) => {
      options?.signal?.addEventListener("abort", () => reject(new Error("timeout")));
    })).mockResolvedValueOnce(new Response("[]"));
    const cache = new JsonResourceCache({ fetcher });
    const rejected = expect(cache.get("/slow")).rejects.toThrow("timeout");
    await vi.advanceTimersByTimeAsync(15_000);
    await rejected;
    await expect(cache.get("/slow")).resolves.toEqual([]);
  });
});
