import { defineConfig } from "vite";

export default defineConfig({
  // The stable loader lives below /catastro_sii_brecha but Vite assets are served
  // from the site-wide /assets tree. Without an explicit base, Vite preloads the
  // lazy MapLibre chunk from /chunks/... and the Jekyll server returns HTML.
  base: "/assets/dist/catastro_sii/",
  publicDir: false,
  build: {
    // Vite 8 raises its defaults. Preserve the browser contract that applied
    // under Vite 7 until the site has a separately reviewed compatibility change.
    target: ["chrome107", "edge107", "firefox104", "safari16"],
    outDir: "assets/dist/catastro_sii",
    emptyOutDir: true,
    manifest: "manifest.json",
    sourcemap: false,
    rolldownOptions: {
      input: "assets/src/catastro_sii/main.ts",
      output: {
        entryFileNames: "[name]-[hash].js",
        chunkFileNames: "chunks/[name]-[hash].js",
        assetFileNames: "[name]-[hash][extname]"
      }
    }
  }
});
