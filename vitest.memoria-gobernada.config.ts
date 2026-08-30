import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "node",
    include: ["tests/memoria_gobernada/**/*.test.ts"]
  }
});
