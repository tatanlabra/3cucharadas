import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "node",
    include: ["tests/catastro_sii/**/*.test.ts"]
  }
});
