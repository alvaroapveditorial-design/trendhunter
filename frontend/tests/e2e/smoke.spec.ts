import { expect, test } from "@playwright/test";

const ingestionButtons = [
  { name: "Run demo ingestion", path: "/api/backend/api/v1/ingestion/demo" },
  { name: "Pull Hacker News", path: "/api/backend/api/v1/ingestion/hackernews" },
  { name: "Pull RSS", path: "/api/backend/api/v1/ingestion/rss" },
  { name: "Pull GitHub", path: "/api/backend/api/v1/ingestion/github" },
];

test("dashboard loads and ingestion actions create pipeline runs", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByRole("heading", { name: "AI Trend Hunter" })).toBeVisible();
  await expect(page.getByText("Recent pipeline runs")).toBeVisible();

  for (const action of ingestionButtons) {
    const button = page.getByRole("button", { name: action.name });
    await expect(button).toBeEnabled();

    const [response] = await Promise.all([
      page.waitForResponse(
        (candidate) =>
          candidate.url().includes(action.path) && candidate.request().method() === "POST"
      ),
      button.click(),
    ]);
    const responseBody = await response.text();
    expect(response.ok(), `${action.name} returned ${response.status()}: ${responseBody}`).toBe(
      true
    );

    await expect(page.getByText(/signals processed/i)).toBeVisible({ timeout: 30000 });
  }

  await expect(page.getByText("Recent pipeline runs")).toBeVisible();
});
