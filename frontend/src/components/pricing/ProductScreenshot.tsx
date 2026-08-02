/**
 * Placeholder for the real dashboard screenshot required by Phoenix Fase 2
 * (section 5.2). No screenshot exists yet -- this must not be filled with
 * invented data. To replace it:
 *
 * 1. Log into the dashboard with an account that has real trend data and no
 *    visible billing/personal information.
 * 2. Capture the "Emerging trends" view at both desktop (~1440px) and mobile
 *    (~390px) widths.
 * 3. Save as frontend/public/pricing/dashboard-preview.png (desktop) and
 *    frontend/public/pricing/dashboard-preview-mobile.png (mobile), optimized
 *    (WebP or compressed PNG, under ~300KB each).
 * 4. Replace this component with a plain <img> using those paths and remove
 *    this placeholder frame.
 */
export function ProductScreenshot() {
  return (
    <section className="section section--tight" id="product-screenshot">
      <div className="container">
        <div className="section-head">
          <span className="eyebrow">Real product view</span>
          <h2 className="h2">What the dashboard actually looks like.</h2>
        </div>
        <div
          role="img"
          aria-label="Real product screenshot pending -- placeholder"
          style={{
            border: "1px dashed var(--line-strong)",
            borderRadius: 10,
            background: "var(--surface-2)",
            padding: "64px 24px",
            textAlign: "center",
            color: "var(--muted)",
          }}
        >
          <p style={{ fontFamily: "var(--mono)", fontSize: 12.5, letterSpacing: ".04em" }}>
            REAL PRODUCT VIEW &mdash; SCREENSHOT PENDING
          </p>
          <p style={{ marginTop: 10, fontSize: 14 }}>
            A real, dated capture of the dashboard is being prepared. See the ranked example
            below for a real opportunity brief in the meantime.
          </p>
        </div>
      </div>
    </section>
  );
}
