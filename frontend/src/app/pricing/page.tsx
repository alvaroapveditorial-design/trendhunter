import { PageViewTracker } from "@/components/PageViewTracker";
import { PricingCheckout } from "@/components/PricingCheckout";

export const metadata = {
  title: "Pricing",
  description: "Try AI Trend Hunter for 7 days and continue with the Pro plan.",
};

export default function PricingPage() {
  return (
    <main className="landing-page pricing-page">
      <PageViewTracker event="Pricing Viewed" />
      <header className="nav">
        <div className="container nav__in">
          <a className="brand" href="/">
            <span className="brand__mark">
              <svg viewBox="0 0 24 24" fill="none">
                <path
                  d="M3 17.5 9.2 11l3.6 3.3L21 6.5"
                  stroke="currentColor"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2.1"
                />
              </svg>
            </span>
            AI Trend Hunter
          </a>
          <div className="nav__cta">
            <a href="/dashboard" className="btn btn--ghost">
              View dashboard
            </a>
          </div>
        </div>
      </header>

      <section className="section pricing-hero">
        <div className="container pricing-hero__grid">
          <div className="pricing-copy">
            <span className="eyebrow">Pro plan</span>
            <h1 className="display">Try AI Trend Hunter for 7 days.</h1>
            <p className="lead">
              Detect emerging SaaS opportunities with public signals, trend scoring, and
              actionable briefs. No open free plan: a short trial to validate real value.
            </p>
            <div className="hero__meta">
              <span>
                <b>39 EUR</b> / month
              </span>
              <span>
                <b>7 days</b> trial
              </span>
              <span>Cancel before the first charge</span>
            </div>
          </div>

          <aside className="pricing-card">
            <div className="pricing-card__top">
              <span className="tag tag--accent">Pro</span>
              <strong>
                39 EUR <small>/month</small>
              </strong>
              <p>First charge after the 7-day trial.</p>
            </div>
            <ul>
              <li>Emerging trends dashboard</li>
              <li>GitHub, Hacker News, and RSS as initial sources</li>
              <li>Opportunity, momentum, and saturation scores</li>
              <li>Actionable briefs for SaaS ideas</li>
              <li>Pipeline run history</li>
            </ul>
            <PricingCheckout />
            <p className="pricing-card__fineprint">
              Checkout is processed with Stripe. Automatic billing starts when the trial
              ends unless you cancel first. By continuing you accept the{" "}
              <a href="/terms">terms</a> and <a href="/privacy">privacy policy</a>.
            </p>
          </aside>
        </div>
      </section>
    </main>
  );
}
