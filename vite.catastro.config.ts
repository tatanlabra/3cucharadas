import { defineConfig } from "vite";

export default defineConfig({
  // The stable loader lives below /catastro_sii_brecha but Vite assets are served
  // from the site-wide /assets tree. Without an explicit base, Vite preloads the
  // lazy MapLibre chunk from /chunks/... and the Jekyll server returns HTML.
  base: "/assets/dist/catastro_sii/",
  publicDir: false,
  build: {
    outDir: "assets/dist/catastro_sii",
    emptyOutDir: true,
    manifest: "manifest.json",
    sourcemap: false,
    rollupOptions: {
      input: "assets/src/catastro_sii/main.ts",
      output: {
        entryFileNames: "[name]-[hash].js",
        chunkFileNames: "chunks/[name]-[hash].js",
        assetFileNames: "[name]-[hash][extname]"
      }
    }
  }
});
