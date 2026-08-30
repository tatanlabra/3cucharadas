import { defineConfig } from "vite";

export default defineConfig({
  base: "/assets/dist/memoria_gobernada/",
  publicDir: false,
  // El límite se acompaña por un gate gzip de 150 KiB; evitar el warning de 500 kB
  // sin comprimir no equivale a renunciar a un presupuesto de transferencia.
  build: {
    // Vite 8 raises its defaults. Keep Vite 7's browser contract explicit
    // while the visualization remains a progressive enhancement.
    target: ["chrome107", "edge107", "firefox104", "safari16"],
    chunkSizeWarningLimit: 550,
    outDir: "assets/dist/memoria_gobernada",
    emptyOutDir: true,
    manifest: "manifest.json",
    sourcemap: false,
    rolldownOptions: {
      input: "assets/src/memoria_gobernada/main.ts",
      output: {
        entryFileNames: "[name]-[hash].js",
        chunkFileNames: "chunks/[name]-[hash].js",
        assetFileNames: "[name]-[hash][extname]"
      }
    }
  }
});
