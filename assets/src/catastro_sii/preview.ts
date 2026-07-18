const LOCAL_PREVIEW_HOSTS = new Set(["localhost", "127.0.0.1", "[::1]"]);
const RUN_ID = /^\d{8}T\d{6}Z$/;

function localPreviewRun(search: string): string | null {
  const query = new URLSearchParams(search);
  const mode = query.get("catastroPreview");
  const run = query.get("run");
  if (mode === null && run === null) return null;
  return mode === "local" && run !== null && RUN_ID.test(run) ? run : null;
}

export function isLocalPreviewLocation(hostname: string, search: string): boolean {
  if (!LOCAL_PREVIEW_HOSTS.has(hostname)) return false;
  const query = new URLSearchParams(search);
  const hasExplicitPreview = query.has("catastroPreview") || query.has("run");
  return !hasExplicitPreview || localPreviewRun(search) !== null;
}

export function manifestUrlForLocation(hostname: string, search: string): string {
  if (isLocalPreviewLocation(hostname, search)) {
    const run = localPreviewRun(search);
    return run
      ? `/assets/data/catastro_sii/local/${run}/manifest.json`
      : "/assets/data/catastro_sii/local/manifest.json";
  }
  return "/assets/data/catastro_sii/manifest.json";
}
