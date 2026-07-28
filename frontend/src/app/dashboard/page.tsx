import { BillingPortalButton } from "@/components/BillingPortalButton";
import { DashboardFilterAnalytics } from "@/components/DashboardFilterAnalytics";
import { LogoutButton } from "@/components/LogoutButton";
import { PageViewTracker } from "@/components/PageViewTracker";
import { TrendDetailAnalytics } from "@/components/TrendDetailAnalytics";
import {
  getCategories,
  getCurrentSession,
  getIngestionRuns,
  getSources,
  getTrend,
  getTrends,
  getTrendSpotlight,
} from "@/lib/api";
import type { Trend, TrendSource } from "@/types/trend";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

export const dynamic = "force-dynamic";

function formatNumber(value: number) {
  return new Intl.NumberFormat("en", { notation: "compact" }).format(value);
}

function scoreTone(score: number) {
  if (score >= 80) return "strong";
  if (score >= 65) return "good";
  return "watch";
}

function formatDateTime(value?: string | null) {
  if (!value) return "Pending";
  return new Intl.DateTimeFormat("en", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function sourceLabel(source?: string | null) {
  if (!source) return "No source";
  if (source === "hackernews") return "Hacker News";
  if (source === "github") return "GitHub";
  if (source === "rss") return "RSS";
  return source.replaceAll("_", " ");
}

function agentLabel(agentName: string) {
  // agent_name is an internal identifier ("mvp_heuristic_detector") -- strip
  // the "mvp" prefix so customers never see internal build-stage naming.
  const cleaned = agentName.replaceAll("_", " ").replace(/^mvp\s+/i, "");
  return cleaned.charAt(0).toUpperCase() + cleaned.slice(1);
}

function sourceMetricsLabel(source: TrendSource) {
  // GitHub and Hacker News reuse the same upvotes/comments fields for
  // different underlying metrics (stars/open issues vs. real upvotes/
  // comments) -- label each source type with what the numbers actually are.
  // RSS's numbers are a synthetic recency estimate, not a real engagement
  // signal, so they're left out entirely rather than shown as if factual.
  if (source.source_type === "github") {
    return `${formatNumber(source.upvotes)} stars · ${formatNumber(source.comments)} open issues`;
  }
  if (source.source_type === "hackernews") {
    return `${formatNumber(source.upvotes)} upvotes · ${formatNumber(source.comments)} comments`;
  }
  return null;
}

function TopFive({
  title,
  trends,
  currentParams,
}: {
  title: string;
  trends: Trend[];
  currentParams: Record<string, string | undefined>;
}) {
  if (trends.length === 0) return null;

  return (
    <div className="top5">
      <h4>{title}</h4>
      <ol>
        {trends.map((trend) => (
          <li key={trend.id}>
            <a
              href={`/dashboard?${new URLSearchParams({
                ...(currentParams.q ? { q: currentParams.q } : {}),
                ...(currentParams.category ? { category: currentParams.category } : {}),
                ...(currentParams.source_type ? { source_type: currentParams.source_type } : {}),
                ...(currentParams.min_score ? { min_score: currentParams.min_score } : {}),
                trend: trend.slug,
              }).toString()}#detail-panel`}
            >
              <span className="top5__score">{Math.round(trend.opportunity_score)}</span>
              <span className="top5__title">{trend.title}</span>
              <span className="top5__cat">{trend.category.replaceAll("_", " ")}</span>
            </a>
          </li>
        ))}
      </ol>
    </div>
  );
}

export default async function DashboardPage({
  searchParams,
}: {
  searchParams?: Promise<{
    q?: string;
    category?: string;
    source_type?: string;
    min_score?: string;
    trend?: string;
  }>;
}) {
  const cookieHeader = (await cookies()).toString();
  let session;
  try {
    session = await getCurrentSession(cookieHeader);
  } catch {
    redirect("/login");
  }
  if (!session.has_active_subscription) {
    redirect("/pricing");
  }

  const params = (await searchParams) ?? {};
  const minScore = params.min_score ? Number(params.min_score) : undefined;
  const [trends, categories, sources, spotlight, runs] = await Promise.all([
    getTrends({
      q: params.q,
      category: params.category,
      sourceType: params.source_type,
      minScore: Number.isNaN(minScore) ? undefined : minScore,
    }),
    getCategories(),
    getSources(),
    getTrendSpotlight(),
    getIngestionRuns(),
  ]);

  // Trust a ?trend= slug even if it comes from the spotlight (top opportunities,
  // emerging markets, etc.) rather than the currently filtered list below --
  // getTrend() resolves it directly against the backend either way. A stale
  // slug (bookmarked link to a since-deactivated trend) must degrade to the
  // top trend, not error the whole page.
  let selectedTrend = params.trend ? await getTrend(params.trend).catch(() => null) : null;
  if (!selectedTrend && trends[0]) {
    selectedTrend = await getTrend(trends[0].slug).catch(() => null);
  }
  const selectedSlug = selectedTrend?.slug;
  const topTrend = trends[0];
  const hasActiveFilters = Boolean(params.q || params.category || params.source_type || params.min_score);
  const brief = spotlight.best_opportunity?.opportunity_brief;

  return (
    <main className="shell">
      <PageViewTracker event="Dashboard Viewed" />
      <DashboardFilterAnalytics />
      <header className="topbar">
        <div>
          <h1>AI Trend Hunter</h1>
        </div>
        <div className="topbar-actions">
          <span>{session.email}</span>
          <BillingPortalButton />
          <LogoutButton />
        </div>
      </header>

      {spotlight.best_opportunity ? (
        <section className="spotlight" aria-label="Best opportunity this week">
          <div className="spotlight-hero">
            <span className="eyebrow">Best opportunity this week</span>
            <h2>{spotlight.best_opportunity.title}</h2>
            {brief ? (
              <>
                <p className="spotlight-hero__summary">{brief.executive_summary}</p>

                <div className="spotlight-scores">
                  <div>
                    <span>Market</span>
                    <strong>{Math.round(brief.scores.market)}</strong>
                  </div>
                  <div>
                    <span>Competition</span>
                    <strong>{Math.round(brief.scores.competition)}</strong>
                  </div>
                  <div>
                    <span>Urgency</span>
                    <strong>{Math.round(brief.scores.urgency)}</strong>
                  </div>
                  <div>
                    <span>Viability</span>
                    <strong>{Math.round(brief.scores.viability)}</strong>
                  </div>
                  <div>
                    <span>Potential</span>
                    <strong>{Math.round(brief.scores.potential)}</strong>
                  </div>
                </div>

                <div className="spotlight-grid">
                  <div className="spotlight-block">
                    <h4>Why now</h4>
                    <p>{brief.why_now}</p>
                  </div>
                  <div className="spotlight-block">
                    <h4>Who would buy it</h4>
                    <p>{brief.icp}</p>
                  </div>
                  <div className="spotlight-block">
                    <h4>Problem it solves</h4>
                    <p>{brief.problem}</p>
                  </div>
                  <div className="spotlight-block">
                    <h4>Competition</h4>
                    <p>{brief.competition_level}</p>
                  </div>
                  <div className="spotlight-block">
                    <h4>Market signal</h4>
                    <p>{brief.market_size_signal}</p>
                  </div>
                  <div className="spotlight-block">
                    <h4>MVP to build</h4>
                    <p>{brief.mvp_recommendation}</p>
                  </div>
                </div>

                <div className="spotlight-lists">
                  <div>
                    <h4>Ways to monetize</h4>
                    <ul>
                      {brief.monetization_models.map((model) => (
                        <li key={model}>{model}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h4>Risks</h4>
                    <ul>
                      {brief.risks.map((risk) => (
                        <li key={risk}>{risk}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </>
            ) : null}
          </div>

          <div className="spotlight-top5-grid">
            <TopFive title="Top 5 opportunities" trends={spotlight.top_opportunities} currentParams={params} />
            <TopFive title="Top 5 emerging markets" trends={spotlight.emerging_markets} currentParams={params} />
            <TopFive title="Top 5 underserved niches" trends={spotlight.underserved_niches} currentParams={params} />
            <TopFive title="Top 5 accelerating" trends={spotlight.accelerating} currentParams={params} />
          </div>
        </section>
      ) : null}

      <p className="eyebrow explore-eyebrow">Explore all trends</p>

      <section className="summary-grid" aria-label="Trend summary">
        <div className="metric">
          <span>Active trends</span>
          <strong>{trends.length}</strong>
        </div>
        <div className="metric">
          <span>Top score</span>
          <strong>{topTrend ? Math.round(topTrend.trend_score) : 0}</strong>
        </div>
        <div className="metric">
          <span>Categories</span>
          <strong>{categories.length}</strong>
        </div>
        <div className="metric">
          <span>Total engagement</span>
          <strong>{formatNumber(trends.reduce((sum, trend) => sum + trend.engagement_count, 0))}</strong>
        </div>
      </section>

      <form className="filters">
        <label>
          Search
          <input name="q" placeholder="copilot, privacy, research..." defaultValue={params.q ?? ""} />
        </label>
        <label>
          Category
          <select name="category" defaultValue={params.category ?? ""}>
            <option value="">All categories</option>
            {categories.map((category) => (
              <option key={category} value={category}>
                {category.replaceAll("_", " ")}
              </option>
            ))}
          </select>
        </label>
        <label>
          Source
          <select name="source_type" defaultValue={params.source_type ?? ""}>
            <option value="">All sources</option>
            {sources.map((source) => (
              <option key={source} value={source}>
                {source === "hackernews" ? "Hacker News" : source}
              </option>
            ))}
          </select>
        </label>
        <label>
          Min score
          <input
            name="min_score"
            type="number"
            min="0"
            max="100"
            step="5"
            defaultValue={params.min_score ?? ""}
            placeholder="0"
          />
        </label>
        <button type="submit">Apply</button>
        {hasActiveFilters ? (
          <a className="clear-filters" href="/dashboard">
            Clear filters
          </a>
        ) : null}
      </form>

      <section className="workspace">
        <div className="trend-list" aria-label="Trend list">
          {trends.length === 0 ? (
            <div className="empty-state">
              <h2>No trends found</h2>
              <p>Try lowering the minimum score or clearing the active filters.</p>
            </div>
          ) : (
            trends.map((trend) => (
              <a
                key={trend.id}
                className={`trend-row ${trend.slug === selectedSlug ? "selected" : ""}`}
                href={`/dashboard?${new URLSearchParams({
                  ...(params.q ? { q: params.q } : {}),
                  ...(params.category ? { category: params.category } : {}),
                  ...(params.source_type ? { source_type: params.source_type } : {}),
                  ...(params.min_score ? { min_score: params.min_score } : {}),
                  trend: trend.slug,
                }).toString()}`}
              >
                <div className={`score ${scoreTone(trend.trend_score)}`}>{Math.round(trend.trend_score)}</div>
                <div className="trend-copy">
                  <div className="row-title">
                    <h2>{trend.title}</h2>
                    {trend.is_verified ? <span>Verified</span> : null}
                  </div>
                  <p>{trend.description}</p>
                  <div className="chips">
                    <span>{sourceLabel(trend.primary_source_type)}</span>
                    <span>{trend.category.replaceAll("_", " ")}</span>
                    <span>{formatNumber(trend.mentions_count)} mentions</span>
                    <span>{formatNumber(trend.engagement_count)} engagement</span>
                  </div>
                </div>
              </a>
            ))
          )}
        </div>

        <aside className="detail-panel" id="detail-panel">
          {selectedTrend ? (
            <>
              <TrendDetailAnalytics
                slug={selectedTrend.slug}
                category={selectedTrend.category}
                hasOpportunities={selectedTrend.saas_opportunities.length > 0}
              />
              <p className="eyebrow">Opportunity brief</p>
              <h2>{selectedTrend.title}</h2>
              <p className="detail-description">{selectedTrend.description}</p>

              <div className="score-grid">
                <div>
                  <span>Trend</span>
                  <strong>{Math.round(selectedTrend.trend_score)}</strong>
                </div>
                <div>
                  <span>Opportunity</span>
                  <strong>{Math.round(selectedTrend.opportunity_score)}</strong>
                </div>
                <div>
                  <span>Saturation</span>
                  <strong>{Math.round(selectedTrend.saturation_score)}</strong>
                </div>
              </div>

              <section className="detail-section">
                <h3>AI insight</h3>
                <p>{selectedTrend.ai_insights}</p>
              </section>

              <section className="detail-section">
                <h3>SaaS opportunities</h3>
                <ul>
                  {selectedTrend.saas_opportunities.map((opportunity) => (
                    <li key={opportunity}>{opportunity}</li>
                  ))}
                </ul>
              </section>

              <section className="detail-section">
                <h3>Source signals</h3>
                {selectedTrend.sources.map((source) => (
                  <div className="source" key={source.id}>
                    <strong>{source.title}</strong>
                    <span>
                      {sourceLabel(source.source_type)}
                      {sourceMetricsLabel(source) ? ` · ${sourceMetricsLabel(source)}` : ""}
                      {source.published_at ? ` · ${formatDateTime(source.published_at)}` : ""}
                    </span>
                  </div>
                ))}
              </section>

              <section className="detail-section">
                <h3>Recent pipeline runs</h3>
                {runs.length === 0 ? (
                  <p>No ingestion runs yet. Run the demo or pull Hacker News to create one.</p>
                ) : (
                  <div className="run-list">
                    {runs.map((run) => (
                      <div className="run-row" key={run.id}>
                        <div>
                          <strong>{agentLabel(run.agent_name)}</strong>
                          <span>
                            {run.records_processed} processed · {run.records_created} created ·{" "}
                            {run.records_updated} updated
                          </span>
                          <time dateTime={run.completed_at ?? run.started_at}>
                            {formatDateTime(run.completed_at ?? run.started_at)}
                          </time>
                        </div>
                        <span className={`run-status ${run.status}`}>{run.status}</span>
                      </div>
                    ))}
                  </div>
                )}
              </section>
            </>
          ) : (
            <div className="empty-state">
              <h2>Select a trend</h2>
              <p>The opportunity brief will appear here.</p>
            </div>
          )}
        </aside>
      </section>
    </main>
  );
}
