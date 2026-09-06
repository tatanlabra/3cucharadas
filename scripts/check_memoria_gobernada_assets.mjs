import { gzipSync } from "node:zlib";
import { readFileSync, realpathSync } from "node:fs";
import { resolve, sep } from "node:path";
import { pathToFileURL } from "node:url";

export function auditBudget(directory, maximum = 150 * 1024) {
  const root = realpathSync(directory);
  const manifest = JSON.parse(readFileSync(resolve(root, "manifest.json"), "utf8"));
  const entries = Object.keys(manifest).filter((key) => manifest[key]?.isEntry);
  if (entries.length === 0) throw new Error("No se encontró una entrada Vite para memoria-gobernada.");
  const visited = new Set();
  const files = new Set();
  const add = (file) => {
    if (typeof file !== "string" || file.startsWith("/") || file.split("/").includes("..")) throw new Error("Asset inseguro");
    const path = realpathSync(resolve(root, file));
    if (!path.startsWith(root + sep)) throw new Error("Asset fuera del bundle");
    files.add(path);
  };
  const visit = (key) => {
    if (visited.has(key)) return;
    visited.add(key);
    const item = manifest[key];
    if (!item?.file) throw new Error(`Import ausente: ${key}`);
    add(item.file);
    for (const file of [...(item.css || []), ...(item.assets || [])]) add(file);
    for (const imported of [...(item.imports || []), ...(item.dynamicImports || [])]) visit(imported);
  };
  entries.forEach(visit);
  const gzipBytes = [...files].reduce((sum, file) => sum + gzipSync(readFileSync(file)).byteLength, 0);
  if (gzipBytes > maximum) throw new Error(`El visor pesa ${gzipBytes} bytes gzip; el presupuesto es ${maximum}.`);
  return { gzipBytes, maximum, files: files.size };
}
if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const result = auditBudget(resolve(process.cwd(), "assets/dist/memoria_gobernada"));
  console.log(`PASS memoria-gobernada graph asset budget: ${result.gzipBytes}/${result.maximum} bytes gzip (${result.files} files)`);
}
