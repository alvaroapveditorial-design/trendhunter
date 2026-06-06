"""Heuristic trend detector for the MVP."""

import logging
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.base import AgentExecution, Trend, TrendSource
from app.schemas.schemas import IngestionRunResponse, SignalBatchIngest, SignalIngest

logger = logging.getLogger(__name__)

# --- Scoring weights (all values sum to 100 max contribution) ---
_SCORE_BASE = 25          # floor score every detected trend starts with
_VELOCITY_CAP = 35        # max points from raw engagement velocity
_VELOCITY_DIVISOR = 8     # engagement units per velocity point
_BREADTH_CAP = 20         # max points from source count diversity
_BREADTH_MULTIPLIER = 5   # source count multiplier for breadth
_RECURRENCE_CAP = 20      # max points from mention recurrence
_RECURRENCE_MULTIPLIER = 4  # mentions multiplier for recurrence
_SATURATION_BASE = 15     # floor saturation every trend starts with
_SATURATION_SOURCE_WEIGHT = 8   # how much each source adds to saturation
_SATURATION_MENTION_WEIGHT = 3  # how much each mention adds to saturation
_OPPORTUNITY_BONUS = 12   # bonus applied before saturation discount
_SATURATION_DISCOUNT = 0.25  # fraction of saturation subtracted from opportunity
_RSS_ENGAGEMENT_FLOOR = 72  # RSS has no votes, so give published items a modest evidence floor
_SOURCE_SCORE_BONUSES = {
    "rss": 8,
}

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "for",
    "from",
    "how",
    "in",
    "into",
    "is",
    "just",
    "more",
    "new",
    "of",
    "on",
    "or",
    "right",
    "that",
    "the",
    "to",
    "use",
    "uses",
    "using",
    "with",
}

CATEGORY_KEYWORDS = {
    "ai_saas": {"ai", "agent", "agents", "automation", "copilot", "llm", "workflow"},
    "privacy": {"cookie", "gdpr", "privacy", "tracking"},
    "product": {"customer", "feedback", "persona", "research", "user"},
    "developer_tools": {"api", "code", "dev", "github", "sdk"},
    "marketing": {"content", "growth", "landing", "seo"},
    "startups": {"battlefield", "founder", "funding", "startup", "startups", "venture"},
    "business": {"business", "company", "market", "revenue", "sales"},
}


def slugify(value: str) -> str:
    """Create a stable URL slug without adding another dependency."""
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return normalized[:80] or f"trend-{uuid4().hex[:8]}"


class DetectorService:
    """Convert raw signals into scored trends."""

    def __init__(self, db: Session):
        self.db = db

    def ingest_batch(self, payload: SignalBatchIngest) -> IngestionRunResponse:
        started_at = datetime.now(timezone.utc).replace(tzinfo=None)
        execution = AgentExecution(
            id=str(uuid4()),
            agent_name="mvp_heuristic_detector",
            agent_type="trend_detector",
            status="running",
            input_params={"signals": len(payload.signals)},
            started_at=started_at,
        )
        self.db.add(execution)
        self.db.flush()

        created = 0
        updated = 0
        touched_trends: list[Trend] = []

        try:
            for signal in payload.signals:
                trend, was_created = self._upsert_signal(signal)
                if was_created:
                    created += 1
                else:
                    updated += 1
                touched_trends.append(trend)

            execution.status = "success"
            execution.completed_at = datetime.now(timezone.utc).replace(tzinfo=None)
            execution.duration_seconds = (execution.completed_at - started_at).total_seconds()
            execution.records_processed = len(payload.signals)
            execution.records_created = created
            execution.records_updated = updated
            execution.created_trend_ids = [trend.id for trend in touched_trends]
            execution.output = {
                "created_trends": created,
                "updated_trends": updated,
                "trend_ids": execution.created_trend_ids,
            }
            self.db.commit()
        except Exception as exc:
            logger.exception("Ingestion batch failed: %s", exc)
            execution.status = "failed"
            execution.completed_at = datetime.now(timezone.utc).replace(tzinfo=None)
            execution.error_message = str(exc)
            self.db.commit()
            raise

        for trend in touched_trends:
            self.db.refresh(trend)

        unique_trends = list({trend.id: trend for trend in touched_trends}.values())
        return IngestionRunResponse(
            processed_signals=len(payload.signals),
            created_trends=created,
            updated_trends=updated,
            trend_ids=[trend.id for trend in unique_trends],
            trends=unique_trends,
        )

    def run_demo(self) -> IngestionRunResponse:
        """Run a deterministic ingestion demo with fresh-ish sample signals."""
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        return self.ingest_batch(
            SignalBatchIngest(
                signals=[
                    SignalIngest(
                        title="Founders are building AI agents for invoice reconciliation",
                        content="Finance teams keep asking for small AI agents that match invoices, receipts, and ERP records.",
                        source_type="demo",
                        source_id=f"demo-finance-agents-{now.date()}",
                        upvotes=146,
                        comments=31,
                        shares=18,
                        keywords=["ai agents", "finance ops", "automation"],
                        category="ai_saas",
                        published_at=now - timedelta(hours=3),
                    ),
                    SignalIngest(
                        title="More indie SaaS teams want privacy-first onboarding analytics",
                        content="Cookie-light activation funnels are getting attention from EU founders.",
                        source_type="demo",
                        source_id=f"demo-privacy-analytics-{now.date()}",
                        upvotes=64,
                        comments=12,
                        shares=6,
                        keywords=["privacy analytics", "onboarding", "gdpr"],
                        category="privacy",
                        published_at=now - timedelta(hours=6),
                    ),
                ]
            )
        )

    def _upsert_signal(self, signal: SignalIngest) -> tuple[Trend, bool]:
        keywords = self._keywords(signal)
        category = signal.category or self._infer_category(keywords)
        title = self._trend_title(signal, keywords)
        slug = slugify(title)
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        engagement = self._signal_engagement(signal)

        trend = self.db.query(Trend).filter(Trend.slug == slug).first()
        was_created = trend is None

        if trend is None:
            trend = Trend(
                id=str(uuid4()),
                title=title,
                slug=slug,
                description=signal.content or signal.title,
                category=category,
                keywords=keywords,
                tags=keywords[:5],
                detected_at=signal.published_at or now,
                expires_at=now + timedelta(days=90),
            )
            self.db.add(trend)
            self.db.flush()

        self._add_source_if_needed(trend, signal)
        self._recalculate_trend(trend, signal, engagement, keywords, category)
        return trend, was_created

    def _add_source_if_needed(self, trend: Trend, signal: SignalIngest) -> None:
        source_id = signal.source_id or slugify(f"{signal.source_type}-{signal.title}")
        existing = (
            self.db.query(TrendSource)
            .filter(
                TrendSource.trend_id == trend.id,
                TrendSource.source_type == signal.source_type,
                TrendSource.source_id == source_id,
            )
            .first()
        )
        if existing:
            return

        self.db.add(
            TrendSource(
                id=str(uuid4()),
                trend_id=trend.id,
                source_type=signal.source_type,
                source_url=signal.source_url,
                source_id=source_id,
                title=signal.title,
                content=signal.content,
                author=signal.author,
                upvotes=signal.upvotes,
                comments=signal.comments,
                shares=signal.shares,
                published_at=signal.published_at,
            )
        )

    def _recalculate_trend(
        self,
        trend: Trend,
        signal: SignalIngest,
        engagement: int,
        keywords: list[str],
        category: str,
    ) -> None:
        all_keywords = sorted(set((trend.keywords or []) + keywords))
        source_count = self.db.query(TrendSource).filter(TrendSource.trend_id == trend.id).count()
        source_count = max(source_count, 1)
        mentions = max(trend.mentions_count or 0, 0) + 1
        total_engagement = max(trend.engagement_count or 0, 0) + engagement

        velocity = min(_VELOCITY_CAP, engagement / _VELOCITY_DIVISOR)
        breadth = min(_BREADTH_CAP, source_count * _BREADTH_MULTIPLIER)
        recurrence = min(_RECURRENCE_CAP, mentions * _RECURRENCE_MULTIPLIER)
        source_bonus = _SOURCE_SCORE_BONUSES.get(signal.source_type, 0)
        score = min(100, _SCORE_BASE + velocity + breadth + recurrence + source_bonus)
        saturation = min(100, _SATURATION_BASE + source_count * _SATURATION_SOURCE_WEIGHT + mentions * _SATURATION_MENTION_WEIGHT)
        opportunity = max(0, min(100, score + _OPPORTUNITY_BONUS - saturation * _SATURATION_DISCOUNT))

        trend.category = category
        trend.keywords = all_keywords
        trend.tags = all_keywords[:6]
        trend.mentions_count = mentions
        trend.engagement_count = total_engagement
        trend.source_count = source_count
        trend.trend_score = round(score, 1)
        trend.opportunity_score = round(opportunity, 1)
        trend.saturation_score = round(saturation, 1)
        trend.momentum = round(velocity, 1)
        trend.content_summary = signal.content or trend.content_summary or signal.title
        trend.ai_insights = self._insight(trend)
        trend.saas_opportunities = self._opportunities(trend)
        trend.last_updated_at = datetime.now(timezone.utc).replace(tzinfo=None)

    def _keywords(self, signal: SignalIngest) -> list[str]:
        explicit = [keyword.strip().lower() for keyword in signal.keywords if keyword.strip()]
        words = re.findall(r"[a-zA-Z][a-zA-Z0-9-]{2,}", f"{signal.title} {signal.content or ''}".lower())
        inferred = [word for word, _ in Counter(word for word in words if word not in STOP_WORDS).most_common(6)]
        return sorted(set(explicit + inferred))[:10]

    def _signal_engagement(self, signal: SignalIngest) -> int:
        engagement = signal.upvotes + signal.comments * 2 + signal.shares * 3
        if signal.source_type == "rss":
            return max(engagement, _RSS_ENGAGEMENT_FLOOR)
        return engagement

    def _infer_category(self, keywords: list[str]) -> str:
        keyword_set = set(" ".join(keywords).replace("-", " ").split())
        if keyword_set.intersection(CATEGORY_KEYWORDS["ai_saas"]):
            return "ai_saas"
        if keyword_set.intersection(CATEGORY_KEYWORDS["developer_tools"]):
            return "developer_tools"
        if keyword_set.intersection(CATEGORY_KEYWORDS["privacy"]):
            return "privacy"
        scores = {
            category: len(keyword_set.intersection(category_keywords))
            for category, category_keywords in CATEGORY_KEYWORDS.items()
        }
        category, score = max(scores.items(), key=lambda item: item[1])
        return category if score > 0 else "emerging"

    def _trend_title(self, signal: SignalIngest, keywords: list[str]) -> str:
        if signal.source_type == "rss":
            return self._rss_trend_title(signal, keywords)
        if signal.keywords:
            return signal.keywords[0].strip().title()
        if keywords:
            return " ".join(keywords[:3]).title()
        return signal.title

    def _rss_trend_title(self, signal: SignalIngest, keywords: list[str]) -> str:
        words = re.findall(r"[a-zA-Z][a-zA-Z0-9-]{1,}", signal.title.lower())
        meaningful = [word for word in words if word not in STOP_WORDS]
        if meaningful:
            return " ".join(meaningful[:5]).title()
        if keywords:
            return " ".join(keywords[:3]).title()
        return signal.title

    def _insight(self, trend: Trend) -> str:
        return (
            f"{trend.title} is showing early signal across {trend.source_count} source(s), "
            f"with {trend.mentions_count} mention(s) and a momentum score of {trend.momentum}."
        )

    def _opportunities(self, trend: Trend) -> list[str]:
        base = trend.title.lower()
        return [
            f"Build a focused monitoring dashboard for {base}",
            f"Create a lightweight workflow tool around {base}",
            f"Package weekly opportunity reports for teams tracking {base}",
        ]
