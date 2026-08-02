import { createReadStream, existsSync, statSync } from "node:fs";
import { createServer } from "node:http";
import { extname, join, normalize, resolve } from "node:path";

const root = resolve(process.argv[2] ?? process.cwd());
const port = Number(process.argv[3] ?? 4014);
const host = process.argv[4] ?? "127.0.0.1";
const overlayRoot = process.argv[5] ? resolve(process.argv[5]) : null;
const localCatastroOverlay = "/assets/data/catastro_sii/local/";

const types = new Map([
  [".html", "text/html; charset=utf-8"],
  [".css", "text/css; charset=utf-8"],
  [".js", "text/javascript; charset=utf-8"],
  [".json", "application/json; charset=utf-8"],
  [".svg", "image/svg+xml"],
  [".png", "image/png"],
  [".jpg", "image/jpeg"],
  [".jpeg", "image/jpeg"],
  [".webp", "image/webp"],
  [".parquet", "application/octet-stream"],
  [".pmtiles", "application/octet-stream"],
  [".woff2", "font/woff2"]
]);

function pathInside(base, pathname) {
  const requested = normalize(decodeURIComponent(pathname)).replace(/^(\.\.[/\\])+/, "");
  const resolved = resolve(join(base, requested));
  if (resolved !== base && !resolved.startsWith(`${base}/`)) return null;
  if (existsSync(resolved) && statSync(resolved).isDirectory()) return join(resolved, "index.html");
  return resolved;
}

function pathFor(url) {
  const parsed = new URL(url, "http://localhost");
  const primary = pathInside(root, parsed.pathname);
  if (primary && existsSync(primary)) return primary;
  if (overlayRoot && parsed.pathname.startsWith(localCatastroOverlay)) {
    return pathInside(overlayRoot, parsed.pathname);
  }
  return primary;
}

createServer((request, response) => {
  const file = pathFor(request.url ?? "/");
  if (!file || !existsSync(file)) {
    response.writeHead(404);
    response.end("not found");
    return;
  }

  const stat = statSync(file);
  const headers = {
    "Accept-Ranges": "bytes",
    "Cache-Control": "no-store",
    "Content-Type": types.get(extname(file)) ?? "application/octet-stream"
  };
  const range = request.headers.range;

  if (range) {
    const match = /^bytes=(\d+)-(\d*)$/.exec(range);
    if (!match) {
      response.writeHead(416, headers);
      response.end();
      return;
    }
    const start = Number(match[1]);
    const end = match[2] ? Number(match[2]) : stat.size - 1;
    if (!Number.isFinite(start) || !Number.isFinite(end) || start > end || end >= stat.size) {
      response.writeHead(416, { ...headers, "Content-Range": `bytes */${stat.size}` });
      response.end();
      return;
    }
    response.writeHead(206, {
      ...headers,
      "Content-Length": end - start + 1,
      "Content-Range": `bytes ${start}-${end}/${stat.size}`
    });
    createReadStream(file, { start, end }).pipe(response);
    return;
  }

  response.writeHead(200, { ...headers, "Content-Length": stat.size });
  createReadStream(file).pipe(response);
}).listen(port, host, () => {
  console.log(`Serving ${root} at http://${host}:${port}/`);
});

process.on("SIGTERM", () => process.exit(0));
