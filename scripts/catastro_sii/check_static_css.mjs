import fs from "node:fs";
import process from "node:process";
import postcss from "postcss";

const stylesheet = process.argv[2];
if (!stylesheet) {
  throw new Error("Uso: node scripts/catastro_sii/check_static_css.mjs <style.css>");
}

postcss.parse(fs.readFileSync(stylesheet, "utf8"));
console.log(`CSS válido: ${stylesheet}`);
