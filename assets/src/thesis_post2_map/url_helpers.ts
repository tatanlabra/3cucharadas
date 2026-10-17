export function resolveAssetTemplate(base: string, path: string): string {
  if (/^https?:\/\//.test(path)) return path;
  return `${base.replace(/\/$/, "")}/${path.replace(/^\/+/, "")}`;
}

export function resolveOrdinaryAsset(base: string, path: string, origin = "https://local.invalid"): string {
  const resolvedBase = new URL(`${base.replace(/\/$/, "")}/`, origin);
  return new URL(path, resolvedBase).toString();
}
