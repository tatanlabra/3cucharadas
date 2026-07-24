const LOCAL_PREVIEW_HOSTS = new Set(["localhost", "127.0.0.1", "[::1]"]);
const RUN_ID = /^\d{8}T\d{6}Z$/;
const PRIVATE_IPV4 = /^(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})$/;

function isPreviewHost(hostname: string): boolean {
  return LOCAL_PREVIEW_HOSTS.has(hostname) || PRIVATE_IPV4.test(hostname);
}

function localPreviewRun(search: string): string | null {
  const query = new URLSearchParams(search);
  const mode = query.get("catastroPreview");
  const run = query.get("run");
  if (mode === null && run === null) return null;
  return mode === "local" && run !== null && RUN_ID.test(run) ? run : null;
}

export function isLocalPreviewLocation(hostname: string, search: string): boolean {
  return isPreviewHost(hostname) && localPreviewRun(search) !== null;
}

export function manifestUrlsForLocation(hostname: string, search: string): string[] {
  if (isLocalPreviewLocation(hostname, search)) {
    const run = localPreviewRun(search);
    return [`/assets/data/catastro_sii/local/${run}/manifest.json`];
  }
  const query = new URLSearchParams(search);
  const invalidExplicitPreview = query.has("catastroPreview") || query.has("run");
  if (isPreviewHost(hostname) && !invalidExplicitPreview) {
    // El overlay local es deliberadamente ajeno al artefacto Jekyll. En el
    // preview 127.0.0.1 evita depender del CORS de R2; si no se preparó, se
    // intenta el manifest público y la interfaz conserva un error legible.
    return [
      "/assets/data/catastro_sii/local/manifest.json",
      "/assets/data/catastro_sii/manifest.json",
    ];
  }
  return ["/assets/data/catastro_sii/manifest.json"];
}

export function manifestUrlForLocation(hostname: string, search: string): string {
  return manifestUrlsForLocation(hostname, search)[0];
}
