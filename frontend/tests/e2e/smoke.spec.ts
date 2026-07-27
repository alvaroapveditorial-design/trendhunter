import { expect, test } from "@playwright/test";

// The dashboard now sits behind email-code auth + an active Stripe
// subscription (see docs/HANDOFF_CTO.md, section 5). Production never
// returns the login code to the client, so a full authenticated run
// through the dashboard isn't something this suite can drive without a
// real inbox. These smoke tests instead cover the parts of the funnel
// that are actually reachable unauthenticated after every deploy: the
// public pages render, and the paywall itself is enforced.

test("landing page renders with the updates signup form", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByRole("heading", { name: "AI Trend Hunter" })).toBeVisible();
  await expect(page.locator("#beta-form")).toBeVisible();
  await expect(page.getByRole("button", { name: "Keep me posted" })).toBeVisible();
});

test("pricing page renders the checkout form", async ({ page }) => {
  await page.goto("/pricing");

  await expect(page.getByRole("heading", { name: /Try AI Trend Hunter/i })).toBeVisible();
  await expect(page.getByLabel("Billing email")).toBeVisible();
  await expect(page.getByRole("button", { name: "Start trial" })).toBeVisible();
});

test("login page renders the email code form", async ({ page }) => {
  await page.goto("/login");

  await expect(page.getByLabel("Email")).toBeVisible();
  await expect(page.getByRole("button", { name: "Send code" })).toBeVisible();
});

test("dashboard redirects unauthenticated visitors instead of leaking data", async ({ page }) => {
  await page.goto("/dashboard");

  await page.waitForURL(/\/(login|pricing)/);
  expect(new URL(page.url()).pathname).toMatch(/^\/(login|pricing)$/);
});
