import { expect, test } from "@playwright/test";

const ingestionButtons = [
  "Run demo ingestion",
  "Pull Hacker News",
  "Pull RSS",
  "Pull GitHub",
];

test("dashboard loads and ingestion actions create pipeline runs", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByRole("heading", { name: "AI Trend Hunter" })).toBeVisible();
  await expect(page.getByText("Recent pipeline runs")).toBeVisible();

  for (const buttonName of ingestionButtons) {
    const button = page.getByRole("button", { name: buttonName });
    await expect(button).toBeEnabled();
    await button.click();
    await expect(page.getByText(/signals processed/i)).toBeVisible();
  }

  await expect(page.getByText("Recent pipeline runs")).toBeVisible();
});
