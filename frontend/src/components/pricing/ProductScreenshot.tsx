/**
 * Real dashboard screenshot for Phoenix Fase 2 (section 5.2). Captured
 * 2026-08-04 from production (aitrendhunter.app/dashboard) using a test
 * account, with the topbar (email + billing button) hidden before the
 * capture so no account/billing info is visible. Shows real trend data.
 *
 * Viewport heights (1440x945 desktop, 390x780 mobile) are chosen to end
 * right after a full card/row -- the first capture cut the "Explore all
 * trends" stat row (desktop) and the "Problem it solves" card (mobile)
 * mid-way, which is what to avoid on any refresh.
 *
 * To refresh: log into the dashboard with an account that has real trend
 * data, hide .topbar, capture at ~1440px and ~390px widths (checking the
 * bottom edge lands between cards, not through one), and replace
 * frontend/public/pricing/dashboard-preview.png (desktop) and
 * dashboard-preview-mobile.png (mobile). Update the caption date below.
 */
export function ProductScreenshot() {
  return (
    <section className="section section--tight" id="product-screenshot">
      <div className="container">
        <div className="section-head">
          <span className="eyebrow">Real product view</span>
          <h2 className="h2">What the dashboard actually looks like.</h2>
        </div>
        <picture>
          <source media="(max-width: 640px)" srcSet="/pricing/dashboard-preview-mobile.png" />
          <img
            src="/pricing/dashboard-preview.png"
            alt="AI Trend Hunter dashboard showing the best opportunity this week and ranked trend shortlists"
            style={{
              width: "100%",
              height: "auto",
              borderRadius: 10,
              border: "1px solid var(--line)",
              display: "block",
            }}
          />
        </picture>
        <p style={{ marginTop: 12, fontSize: 13, color: "var(--muted)" }}>
          Dashboard snapshot captured on 4 August 2026.
        </p>
      </div>
    </section>
  );
}
