import { expect, test } from "@playwright/test";

// The dashboard now sits behind email-code auth + an active Stripe
// subscription (see docs/HANDOFF_CTO.md, section 5). Production never
// returns the login code to the client, so a full authenticated run
// through the dashboard isn't something this suite can drive without a
// real inbox. These smoke tests instead cover the parts of the funnel
// that are actually reachable unauthenticated after every deploy: the
// public pages render, the paywall itself is enforced, and the Phoenix
// Fase 2 conversion additions on /pricing work end to end.

async function stubPlausible(page: import("@playwright/test").Page) {
  await page.addInitScript(() => {
    (window as unknown as { __plausibleCalls: Array<{ event: string; props?: unknown }> }).__plausibleCalls = [];
    (window as unknown as { plausible: (event: string, opts?: { props?: unknown }) => void }).plausible = (
      event,
      opts,
    ) => {
      (window as unknown as { __plausibleCalls: Array<{ event: string; props?: unknown }> }).__plausibleCalls.push({
        event,
        props: opts?.props,
      });
    };
  });
}

test("landing page renders with the updates signup form", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByRole("heading", { name: "AI Trend Hunter" })).toBeVisible();
  await expect(page.locator("#beta-form")).toBeVisible();
  await expect(page.getByRole("button", { name: "Keep me posted" })).toBeVisible();
});

test("pricing page loads and fires Pricing View", async ({ page }) => {
  await stubPlausible(page);
  await page.goto("/pricing");

  await expect(
    page.getByRole("heading", { name: /See what developers are building/i }),
  ).toBeVisible();
  await expect(page.getByLabel("Billing email")).toBeVisible();
  await expect(page.getByRole("button", { name: "Start trial" })).toBeVisible();

  const calls = await page.evaluate(
    () => (window as unknown as { __plausibleCalls: Array<{ event: string }> }).__plausibleCalls,
  );
  expect(calls.filter((c) => c.event === "Pricing View")).toHaveLength(1);
});

test("pricing page shows a real, captioned dashboard screenshot", async ({ page }) => {
  await page.goto("/pricing");

  const section = page.locator("#product-screenshot");
  const img = section.locator("img");
  await expect(img).toBeVisible();
  expect(await img.evaluate((el: HTMLImageElement) => el.naturalWidth)).toBeGreaterThan(0);
  await expect(section.getByText(/Dashboard snapshot captured on/i)).toBeVisible();
});

test("pricing page shows the real, dated opportunity example", async ({ page }) => {
  await page.goto("/pricing");

  const example = page.locator("#real-example");
  await expect(example.getByRole("heading", { name: "Llmgateway" })).toBeVisible();
  await expect(example.getByText(/detected/i).first()).toBeVisible();
  await expect(example.getByText(/theopenco\/llmgateway/i)).toBeVisible();
});

test("pricing page FAQ answers the required questions", async ({ page }) => {
  await page.goto("/pricing");

  const faq = page.locator("#faq");
  const billingQuestion = faq.getByText("Am I charged today?");
  await expect(billingQuestion).toBeVisible();
  await billingQuestion.click();
  await expect(
    faq.getByText("Your first charge happens when the 7-day trial ends"),
  ).toBeVisible();
});

test("How it works nav link scrolls to the mechanism section and fires How It Works Click", async ({ page }) => {
  await stubPlausible(page);
  await page.goto("/pricing");

  await page.getByRole("link", { name: "How it works" }).click();
  await expect(page.locator("#mechanism")).toBeInViewport();

  const calls = await page.evaluate(
    () => (window as unknown as { __plausibleCalls: Array<{ event: string }> }).__plausibleCalls,
  );
  expect(calls.filter((c) => c.event === "How It Works Click")).toHaveLength(1);
});

test("valid email creates a checkout session and fires the checkout events once", async ({ page }) => {
  await stubPlausible(page);
  await page.route("**/api/backend/api/v1/billing/checkout", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      // A same-page hash so the app's `window.location.href = checkout_url`
      // redirect only changes the fragment instead of loading a new
      // document -- a real Stripe URL would tear down the page (and the
      // stubbed window.plausible) before we can inspect the tracked calls.
      body: JSON.stringify({ checkout_url: "/pricing#mock-checkout", session_id: "cs_test_123" }),
    });
  });

  await page.goto("/pricing");
  await page.getByLabel("Billing email").fill("smoke-test@example.com");
  await page.getByRole("button", { name: "Start trial" }).click();

  await page.waitForURL("**/pricing#mock-checkout");

  const calls = await page.evaluate(
    () => (window as unknown as { __plausibleCalls: Array<{ event: string }> }).__plausibleCalls,
  );
  for (const eventName of ["Pricing CTA Clicked", "Checkout Started", "Checkout Created"]) {
    expect(calls.filter((c) => c.event === eventName)).toHaveLength(1);
  }
});

test("a rejected email shows an inline error instead of redirecting", async ({ page }) => {
  await page.route("**/api/backend/api/v1/billing/checkout", async (route) => {
    await route.fulfill({
      status: 409,
      contentType: "application/json",
      body: JSON.stringify({ detail: "You already have an active subscription for this email." }),
    });
  });

  await page.goto("/pricing");
  await page.getByLabel("Billing email").fill("already-subscribed@example.com");
  await page.getByRole("button", { name: "Start trial" }).click();

  await expect(page.getByText("You already have an active subscription for this email.")).toBeVisible();
  expect(page.url()).toContain("/pricing");
});

test("pricing page has no dead links", async ({ page }) => {
  await page.goto("/pricing");

  const hrefs = await page.locator("a[href]").evaluateAll((links) => links.map((l) => l.getAttribute("href")));
  for (const href of hrefs) {
    expect(href).not.toBe("#");
    expect(href).not.toBeNull();
    expect(href?.trim()).not.toBe("");
  }
});

test("pricing page renders correctly on mobile", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/pricing");

  await expect(
    page.getByRole("heading", { name: /See what developers are building/i }),
  ).toBeVisible();
  await expect(page.getByLabel("Billing email")).toBeVisible();

  const hasHorizontalOverflow = await page.evaluate(
    () => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
  );
  expect(hasHorizontalOverflow).toBe(false);
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
