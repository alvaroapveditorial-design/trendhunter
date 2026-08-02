import { PageViewTracker } from "@/components/PageViewTracker";

/**
 * A real, dated opportunity brief pulled from production on 2026-08-02 (see
 * /phoenix/PHASE_2_IMPLEMENTATION_PLAN.md for the source query and how to
 * refresh this). Static rather than live because /api/v1/trends requires the
 * internal server-to-server key and isn't safe to expose publicly.
 */
const EXAMPLE = {
  title: "Llmgateway",
  detectedAt: "July 31, 2026",
  description:
    "Route, manage, and analyze LLM requests across multiple providers with a unified API interface.",
  category: "AI infra",
  scores: { opportunity: 88, saturation: 29, momentum: 33.2 },
  icp: "Product and engineering teams who want AI in their product without building the infrastructure themselves",
  problem: "Adopting AI capabilities without spending months building the infrastructure in-house",
  mvp: "A focused monitoring dashboard for LLM gateway usage",
  risk: "Single-source signal so far — worth validating with additional data before investing",
  source: {
    type: "GitHub",
    label: "theopenco/llmgateway",
    url: "https://github.com/theopenco/llmgateway",
    stars: 1486,
    openIssues: 54,
  },
};

export function RealExampleCard() {
  return (
    <section className="section" id="real-example">
      <div className="container">
        <div className="section-head">
          <span className="eyebrow">Real example, not a mockup</span>
          <h2 className="h2">One opportunity brief straight from the product.</h2>
          <p className="lead">
            Detected on {EXAMPLE.detectedAt} from real public activity. Not a live number — a
            dated capture so you can see the actual shape of a brief before you pay for one.
          </p>
        </div>

        <article className="scard" style={{ maxWidth: 640 }}>
          <div className="scard__top">
            <div className="scard__big">
              {EXAMPLE.scores.opportunity}
              <small>/100</small>
            </div>
            <span className="tag tag--accent">Opportunity score</span>
          </div>
          <h3>{EXAMPLE.title}</h3>
          <div className="scard__cat">
            {EXAMPLE.category} &middot; detected {EXAMPLE.detectedAt}
          </div>
          <p className="scard__brief">{EXAMPLE.description}</p>

          <div className="scard__scores">
            <div className="scard__score">
              <label>Opportunity</label>
              <div className="meter__bar">
                <div
                  className="meter__fill meter__fill--accent"
                  style={{ ["--val" as string]: `${EXAMPLE.scores.opportunity}%` }}
                />
              </div>
              <b>{EXAMPLE.scores.opportunity}</b>
            </div>
            <div className="scard__score">
              <label>Saturation</label>
              <div className="meter__bar">
                <div
                  className="meter__fill meter__fill--pos"
                  style={{ ["--val" as string]: `${EXAMPLE.scores.saturation}%` }}
                />
              </div>
              <b>{EXAMPLE.scores.saturation}</b>
            </div>
            <div className="scard__score">
              <label>Momentum</label>
              <div className="meter__bar">
                <div
                  className="meter__fill meter__fill--pos"
                  style={{ ["--val" as string]: `${Math.min(EXAMPLE.scores.momentum, 100)}%` }}
                />
              </div>
              <b>{EXAMPLE.scores.momentum}</b>
            </div>
          </div>

          <ul style={{ display: "grid", gap: 8, listStyle: "none", padding: 0, margin: "16px 0" }}>
            <li>
              <b>Possible customer:</b> {EXAMPLE.icp}
            </li>
            <li>
              <b>Problem:</b> {EXAMPLE.problem}
            </li>
            <li>
              <b>Possible MVP:</b> {EXAMPLE.mvp}
            </li>
            <li>
              <b>Main risk:</b> {EXAMPLE.risk}
            </li>
          </ul>

          <div className="scard__foot">
            <div className="scard__sources">
              <span className="src src--gh">
                <i></i>
                {EXAMPLE.source.label} &middot; {EXAMPLE.source.stars.toLocaleString()} stars &middot;{" "}
                {EXAMPLE.source.openIssues} open issues
              </span>
            </div>
            <a
              href={EXAMPLE.source.url}
              className="scard__link"
              target="_blank"
              rel="noopener noreferrer"
            >
              View source
            </a>
          </div>
        </article>

        <PageViewTracker event="Real Example Viewed" props={{ example_slug: "llmgateway" }} />
      </div>
    </section>
  );
}
