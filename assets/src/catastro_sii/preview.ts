const LOCAL_PREVIEW_HOSTS = new Set(["localhost", "127.0.0.1", "[::1]"]);
const RUN_ID = /^\d{8}T\d{6}Z$/;

export function manifestUrlForLocation(hostname: string, search: string): string {
  const query = new URLSearchParams(search);
  const run = query.get("run");
  if (
    LOCAL_PREVIEW_HOSTS.has(hostname)
    && query.get("catastroPreview") === "local"
    && run !== null
    && RUN_ID.test(run)
  ) {
    return `/assets/data/catastro_sii/local/${run}/manifest.json`;
  }
  return "/assets/data/catastro_sii/manifest.json";
}
