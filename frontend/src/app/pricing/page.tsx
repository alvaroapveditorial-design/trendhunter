import { PageViewTracker } from "@/components/PageViewTracker";
import { PricingCheckout } from "@/components/PricingCheckout";
import { PricingAnalytics } from "@/components/pricing/PricingAnalytics";
import { ProductScreenshot } from "@/components/pricing/ProductScreenshot";
import { RealExampleCard } from "@/components/pricing/RealExampleCard";
import { PricingFaq } from "@/components/pricing/PricingFaq";

export const metadata = {
  title: "Pricing",
  description: "See a real opportunity brief before you start the 7-day trial.",
};

const MECHANISM_STEPS = [
  {
    step: "01",
    title: "Collect public signals",
    body: "We continuously read GitHub repos, Hacker News threads, and RSS feeds -- the public places builders talk before anything trends.",
  },
  {
    step: "02",
    title: "Filter out the noise",
    body: "Spam, unrelated activity, and low-signal mentions get filtered before anything reaches scoring.",
  },
  {
    step: "03",
    title: "Group related signals",
    body: "Mentions of the same underlying idea across sources are grouped into a single trend instead of scattered data points.",
  },
  {
    step: "04",
    title: "Score momentum, opportunity, and saturation",
    body: "Each trend gets three numbers, so comparing ideas is a glance instead of a judgment call.",
  },
  {
    step: "05",
    title: "Turn it into an actionable brief",
    body: "The strongest trends become a short brief: who it's for, why now, and where the gap is.",
  },
];

const AVAILABLE_TODAY = [
  "Opportunities dashboard, ranked by score",
  "Prioritized, sortable trend list",
  "Signal sources: GitHub, Hacker News, and RSS",
  "Actionable briefs: ICP, competition, MVP, monetization, and risks",
  "Momentum, opportunity, and saturation scoring",
];

const COMING_SOON = ["Alerts", "PDF export", "Watchlists", "Automated reports", "Integrations"];

export default function PricingPage() {
  return (
    <main className="landing-page pricing-page">
      <PageViewTracker event="Pricing View" />
      <PricingAnalytics />
      <header className="nav" id="nav">
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
          <nav className="nav__links">
            <a href="/">Home</a>
            <a href="#mechanism" data-track="how-it-works">
              How it works
            </a>
            <a href="#real-example">Real example</a>
            <a href="#faq">FAQ</a>
          </nav>
          <div className="nav__cta">
            <a href="/dashboard" className="btn btn--ghost">
              View dashboard
            </a>
            <a href="#checkout" className="btn btn--primary">
              Start 7-day trial
            </a>
          </div>
        </div>
      </header>

      <section className="section pricing-hero">
        <div className="container pricing-hero__grid">
          <div className="pricing-copy">
            <span className="eyebrow">For builders picking their next SaaS bet</span>
            <h1 className="display">
              See what developers are building before it's a search trend.
            </h1>
            <p className="lead">
              AI Trend Hunter reads GitHub repos, Hacker News threads, and RSS feeds -- where
              new ideas show up in code and conversation first -- and turns that public signal
              into scored, actionable opportunity briefs.
            </p>
            <div className="hero__meta">
              <span>
                <b>3</b> public sources
              </span>
              <span>
                <b>7 days</b> free trial
              </span>
              <span>39 EUR/month after, cancel before the first charge</span>
            </div>
          </div>

          <aside className="pricing-card" id="checkout">
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

      <ProductScreenshot />

      <RealExampleCard />

      <section className="section section--tight" id="mechanism">
        <div className="container">
          <div className="section-head">
            <span className="eyebrow">How it works</span>
            <h2 className="h2">From public signal to a decision, in five steps.</h2>
          </div>
          <div style={{ display: "grid", gap: 20 }}>
            {MECHANISM_STEPS.map((item) => (
              <div key={item.step} className="pipe__step" style={{ maxWidth: 640 }}>
                <div className="pipe__k">STEP {item.step}</div>
                <h3>{item.title}</h3>
                <p>{item.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section
        className="section section--tight"
        style={{ background: "var(--surface-2)", borderTop: "1px solid var(--line)", borderBottom: "1px solid var(--line)" }}
      >
        <div className="container">
          <div className="section-head">
            <span className="eyebrow">What you get today</span>
            <h2 className="h2">Built and working right now.</h2>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 32 }}>
            <div>
              <h3 style={{ fontSize: 15, marginBottom: 12 }}>Available today</h3>
              <ul style={{ display: "grid", gap: 10, listStyle: "none", padding: 0 }}>
                {AVAILABLE_TODAY.map((item) => (
                  <li key={item} style={{ fontSize: 15, color: "var(--ink-soft)" }}>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h3 style={{ fontSize: 15, marginBottom: 12, color: "var(--muted)" }}>Coming soon</h3>
              <ul style={{ display: "grid", gap: 10, listStyle: "none", padding: 0 }}>
                {COMING_SOON.map((item) => (
                  <li key={item}>
                    <span className="tag">{item} -- coming soon</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </section>

      <PricingFaq />
    </main>
  );
}
