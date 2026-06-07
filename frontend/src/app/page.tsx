import { IngestionActions } from "@/components/IngestionActions";
import { getCategories, getIngestionRuns, getSources, getTrend, getTrends } from "@/lib/api";

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
  const params = (await searchParams) ?? {};
  const minScore = params.min_score ? Number(params.min_score) : undefined;
  const [trends, categories, sources] = await Promise.all([
    getTrends({
      q: params.q,
      category: params.category,
      sourceType: params.source_type,
      minScore: Number.isNaN(minScore) ? undefined : minScore,
    }),
    getCategories(),
    getSources(),
  ]);
  const runs = await getIngestionRuns();

  const selectedSlug =
    params.trend && trends.some((trend) => trend.slug === params.trend)
      ? params.trend
      : trends[0]?.slug;
  const selectedTrend = selectedSlug ? await getTrend(selectedSlug) : null;
  const topTrend = trends[0];
  const hasActiveFilters = Boolean(params.q || params.category || params.source_type || params.min_score);

  return (
    <main className="shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">MVP Dashboard</p>
          <h1>AI Trend Hunter</h1>
        </div>
        <a className="docs-link" href="http://localhost:8000/docs">
          API Docs
        </a>
      </header>

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
          <a className="clear-filters" href="/">
            Clear filters
          </a>
        ) : null}
      </form>

      <section className="ingestion-panel">
        <div>
          <p className="eyebrow">Detection pipeline</p>
          <h2>Turn public signals into scored trends</h2>
          <p>
            Run the detector with sample signals or pull live Hacker News stories. It creates
            or updates trends, sources, scores, opportunities, and agent execution logs.
          </p>
          <div className="pipeline-meta">
            <span>Protected ingestion</span>
            <span>{runs[0] ? `Last run ${formatDateTime(runs[0].completed_at ?? runs[0].started_at)}` : "No runs yet"}</span>
          </div>
        </div>
        <IngestionActions />
      </section>

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
                href={`/?${new URLSearchParams({
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

        <aside className="detail-panel">
          {selectedTrend ? (
            <>
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
                      {sourceLabel(source.source_type)} · {formatNumber(source.upvotes)} upvotes ·{" "}
                      {formatNumber(source.comments)} comments
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
                          <strong>{run.agent_name.replaceAll("_", " ")}</strong>
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
