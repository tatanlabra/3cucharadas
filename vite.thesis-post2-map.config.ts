import { defineConfig } from "vite";

export default defineConfig({
  base: "/assets/dist/thesis_post2_map/",
  publicDir: false,
  build: {
    target: ["chrome107", "edge107", "firefox104", "safari16"],
    outDir: "assets/dist/thesis_post2_map",
    emptyOutDir: true,
    manifest: "manifest.json",
    sourcemap: false,
    rolldownOptions: {
      input: "assets/src/thesis_post2_map/main.ts",
      output: {
        entryFileNames: "[name]-[hash].js",
        chunkFileNames: "chunks/[name]-[hash].js",
        assetFileNames: "[name]-[hash][extname]"
      }
    }
  }
});
