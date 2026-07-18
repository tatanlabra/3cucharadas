import { defineConfig } from "vite";

export default defineConfig({
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
