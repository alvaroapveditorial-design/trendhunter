import { defineConfig, devices } from "@playwright/test";

const baseURL = process.env.PLAYWRIGHT_BASE_URL ?? "https://trendhunter-frontend-production.up.railway.app";

export default defineConfig({
  testDir: "./tests/e2e",
  timeout: 90_000,
  expect: {
    timeout: 15_000,
  },
  use: {
    baseURL,
    trace: "retain-on-failure",
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
});
