import { gzipSync } from "node:zlib";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = process.cwd();
const manifestPath = resolve(root, "assets/dist/memoria_gobernada/manifest.json");
const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
const entry = Object.values(manifest).find((item) => item && item.isEntry);
if (!entry?.file) throw new Error("No se encontró una entrada Vite para memoria-gobernada.");

const asset = readFileSync(resolve(root, "assets/dist/memoria_gobernada", entry.file));
const gzipBytes = gzipSync(asset).byteLength;
const maximum = 150 * 1024;
if (gzipBytes > maximum) {
  throw new Error(`El visor pesa ${gzipBytes} bytes gzip; el presupuesto es ${maximum}.`);
}
console.log(`PASS memoria-gobernada asset budget: ${gzipBytes}/${maximum} bytes gzip`);
