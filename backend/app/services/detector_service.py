"""Heuristic trend detector for the MVP."""

import logging
import math
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.base import AgentExecution, Trend, TrendSource
from app.schemas.schemas import IngestionRunResponse, SignalBatchIngest, SignalIngest
from app.services.text_filters import RELEVANCE_TERMS, looks_non_english

logger = logging.getLogger(__name__)

# Collectors already filter for relevance/language before building a signal,
# but the admin-only /ingestion/signals endpoint accepts raw signals directly
# and bypasses that -- so this is the one choke point every signal passes
# through no matter how it got here. GitHub signals aren't checked for topic
# relevance: the search query (topic:ai) already scopes them.
_RELEVANCE_CHECKED_SOURCES = {"hackernews", "rss"}


def _passes_content_quality_gate(signal: SignalIngest) -> bool:
    haystack = f"{signal.title} {signal.content or ''}"
    if looks_non_english(haystack):
        return False
    if signal.source_type in _RELEVANCE_CHECKED_SOURCES:
        if not any(term in haystack.lower() for term in RELEVANCE_TERMS):
            return False
    return True

# --- Scoring weights (all values sum to 100 max contribution) ---
_SCORE_BASE = 25          # floor score every detected trend starts with
_VELOCITY_CAP = 35        # max points from raw engagement velocity
_VELOCITY_LOG_MULTIPLIER = 10  # log10(engagement) points per order of magnitude
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
    "github": 12,
    "rss": 8,
}

GENERIC_TITLE_KEYWORDS = {
    "ai",
    "agent",
    "agents",
    "code",
    "developer tools",
    "github",
    "product",
    "saas",
    "software",
    "startup",
    "startups",
}

STOP_WORDS = {
    "a",
    "an",
    "and",
    "another",
    "are",
    "as",
    "at",
    "any",
    "be",
    "been",
    "being",
    "but",
    "by",
    "can",
    "could",
    "did",
    "do",
    "does",
    "don",
    "during",
    "each",
    "for",
    "from",
    "get",
    "has",
    "have",
    "having",
    "how",
    "in",
    "into",
    "is",
    "it",
    "just",
    "know",
    "link",
    "longer",
    "make",
    "many",
    "me",
    "more",
    "most",
    "my",
    "new",
    "not",
    "now",
    "of",
    "on",
    "or",
    "our",
    "own",
    "please",
    "problem",
    "right",
    "ship",
    "show",
    "shot",
    "some",
    "than",
    "that",
    "th",
    "the",
    "their",
    "these",
    "they",
    "this",
    "to",
    "use",
    "uses",
    "using",
    "want",
    "was",
    "were",
    "what",
    "when",
    "where",
    "who",
    "why",
    "with",
    "you",
    "your",
}

CATEGORY_PROFILES = {
    "ai_saas": {
        "icp": "Product and engineering teams who want AI in their product without building the infrastructure themselves",
        "problem": "Adopting AI capabilities without spending months building the infrastructure in-house",
        "monetization_models": [
            "SaaS monthly subscription",
            "Usage-based API pricing",
            "Add-on/plugin for existing tools",
        ],
        "viability_bonus": 25,
    },
    "developer_tools": {
        "icp": "Developers and platform teams",
        "problem": "No standard, reliable tool exists yet for this workflow",
        "monetization_models": [
            "Open-core with paid support",
            "Per-seat SaaS",
            "Paid API/SDK usage",
        ],
        "viability_bonus": 25,
    },
    "privacy": {
        "icp": "Product and legal teams at companies with compliance requirements (GDPR)",
        "problem": "Meeting privacy regulation without sacrificing product functionality or analytics",
        "monetization_models": ["SaaS subscription", "Audit/consulting bundled with a tool"],
        "viability_bonus": 15,
    },
    "product": {
        "icp": "Product managers and research teams",
        "problem": "Understanding the user faster with less manual research effort",
        "monetization_models": ["SaaS subscription", "User-research add-on"],
        "viability_bonus": 15,
    },
    "marketing": {
        "icp": "Marketing and growth teams at startups",
        "problem": "Getting more output with less manual effort in their marketing stack",
        "monetization_models": ["SaaS subscription", "Managed service bundled with a tool"],
        "viability_bonus": 15,
    },
    "startups": {
        "icp": "Founders and early-stage teams",
        "problem": "Validating or shipping faster with limited resources",
        "monetization_models": ["SaaS subscription", "Community + tool (freemium)"],
        "viability_bonus": 10,
    },
    "business": {
        "icp": "Operations and business teams at SMBs",
        "problem": "Manual processes eating up the team's time",
        "monetization_models": ["SaaS subscription", "Service bundled with software"],
        "viability_bonus": 10,
    },
}

_DEFAULT_CATEGORY_PROFILE = {
    "icp": "Early adopters of this space -- no defined profile yet",
    "problem": "Emerging need detected from public signal, not validated yet",
    "monetization_models": ["To be validated -- not enough signal to recommend a model yet"],
    "viability_bonus": 0,
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


_ACRONYMS = {"ai", "api", "sdk", "gdpr", "llm", "saas", "seo", "ui", "ux", "qa", "crm", "erp", "mvp", "sql", "aws"}


def _titlecase(value: str) -> str:
    """Title-case a phrase while keeping known tech acronyms fully uppercase.

    Python's str.title() turns "ai agents" into "Ai Agents" -- wrong for a
    product whose whole premise is AI trends. Fixes the common ones without
    a full NLP dependency.
    """
    return " ".join(word.upper() if word.lower() in _ACRONYMS else word for word in value.title().split())


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
                if not _passes_content_quality_gate(signal):
                    continue
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
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        engagement = self._signal_engagement(signal)

        trend = self._find_existing_trend(signal, title)
        was_created = trend is None

        if trend is None:
            trend = Trend(
                id=str(uuid4()),
                title=title,
                slug=self._unique_slug(slugify(title)),
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

    def _find_existing_trend(self, signal: SignalIngest, title: str) -> Trend | None:
        """Match a signal to an existing trend.

        A concrete source (e.g. one GitHub repo) always maps back to whichever
        trend it was already attached to, regardless of how the title heuristic
        scores it on this run -- prevents the same repo from splitting into two
        trends, or two unrelated repos merging because they guessed the same title.
        GitHub signals never fall back to title-slug matching: a repo is its own
        entity and should never cluster with another repo by guessed title alone.
        """
        source_id = signal.source_id or slugify(f"{signal.source_type}-{signal.title}")
        existing_source = (
            self.db.query(TrendSource)
            .filter(TrendSource.source_type == signal.source_type, TrendSource.source_id == source_id)
            .first()
        )
        if existing_source:
            return self.db.query(Trend).filter(Trend.id == existing_source.trend_id).first()

        if signal.source_type == "github":
            return None

        return self.db.query(Trend).filter(Trend.slug == slugify(title)).first()

    def _unique_slug(self, base_slug: str) -> str:
        slug = base_slug
        suffix = 2
        while self.db.query(Trend).filter(Trend.slug == slug).first() is not None:
            slug = f"{base_slug}-{suffix}"
            suffix += 1
        return slug

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
        all_keywords = self._clean_keywords_list((trend.keywords or []) + keywords)
        source_count = self.db.query(TrendSource).filter(TrendSource.trend_id == trend.id).count()
        source_count = max(source_count, 1)
        mentions = max(trend.mentions_count or 0, 0) + 1
        total_engagement = max(trend.engagement_count or 0, 0) + engagement

        # Engagement (stars, upvotes, forks...) follows a power-law distribution,
        # not a linear one: the gap between 50 and 500 is far more meaningful
        # than between 2500 and 3000. A linear divisor saturated the cap almost
        # immediately for any repo past a few hundred stars, making unrelated
        # trends land on the exact same score -- log-scaling spreads the whole
        # practical range out instead of flattening most of it to the ceiling.
        velocity = min(_VELOCITY_CAP, math.log10(engagement + 1) * _VELOCITY_LOG_MULTIPLIER)
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
        trend.opportunity_brief = self._build_opportunity_brief(trend)
        trend.last_updated_at = datetime.now(timezone.utc).replace(tzinfo=None)

    def _keywords(self, signal: SignalIngest) -> list[str]:
        explicit = [
            keyword.strip().lower()
            for keyword in signal.keywords
            if self._is_meaningful_keyword(keyword)
        ]
        words = re.findall(r"[a-zA-Z][a-zA-Z0-9-]{2,}", f"{signal.title} {signal.content or ''}".lower())
        inferred = [word for word, _ in Counter(word for word in words if word not in STOP_WORDS).most_common(6)]
        return self._clean_keywords_list(explicit + inferred)[:10]

    def _clean_keywords_list(self, keywords: list[str]) -> list[str]:
        cleaned = []
        for keyword in keywords:
            normalized = keyword.strip().lower()
            if self._is_meaningful_keyword(normalized):
                cleaned.append(normalized)
        return sorted(set(cleaned))

    def _is_meaningful_keyword(self, keyword: str) -> bool:
        normalized = keyword.strip().lower()
        if not normalized:
            return False
        words = re.findall(r"[a-zA-Z][a-zA-Z0-9-]{1,}", normalized)
        return any(word not in STOP_WORDS for word in words)

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
        if signal.source_type == "github":
            return self._github_trend_title(signal, keywords)
        if signal.source_type == "rss":
            return self._rss_trend_title(signal, keywords)
        explicit = [keyword.strip().lower() for keyword in signal.keywords if self._is_title_keyword(keyword)]
        if explicit:
            return _titlecase(explicit[0])
        return self._title_from_signal(signal.title, keywords)

    def _is_title_keyword(self, keyword: str) -> bool:
        normalized = keyword.strip().lower()
        if not self._is_meaningful_keyword(normalized):
            return False
        return normalized not in GENERIC_TITLE_KEYWORDS

    def _title_from_signal(self, title: str, keywords: list[str], max_words: int = 5) -> str:
        words = re.findall(r"[a-zA-Z][a-zA-Z0-9-]{1,}", title.lower())
        meaningful = [word for word in words if word not in STOP_WORDS]
        if meaningful:
            return _titlecase(" ".join(meaningful[:max_words]))
        title_keywords = [keyword for keyword in keywords if keyword not in GENERIC_TITLE_KEYWORDS]
        if title_keywords:
            return _titlecase(" ".join(title_keywords[:3]))
        if keywords:
            return _titlecase(" ".join(keywords[:3]))
        return title

    def _rss_trend_title(self, signal: SignalIngest, keywords: list[str]) -> str:
        return self._title_from_signal(signal.title, keywords)

    def _github_trend_title(self, signal: SignalIngest, keywords: list[str]) -> str:
        repo_name = signal.title.rsplit("/", 1)[-1].replace("-", " ").replace("_", " ")
        title = self._title_from_signal(repo_name, keywords, max_words=4)
        return title if title.lower() not in GENERIC_TITLE_KEYWORDS else self._title_from_signal(signal.title, keywords)

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

    def _build_opportunity_brief(self, trend: Trend) -> dict:
        """Turn a scored trend into a decision-oriented brief.

        Deliberately heuristic, not LLM-generated: every field is derived
        from data already computed for this trend (scores, source count,
        category), so there is no per-trend inference cost and nothing here
        claims to be an AI-verified fact -- it's the same explainable
        scoring approach as trend_score/opportunity_score, just structured
        as a brief instead of four numbers.
        """
        profile = CATEGORY_PROFILES.get(trend.category, _DEFAULT_CATEGORY_PROFILE)

        market = round(min(100, trend.source_count * _BREADTH_MULTIPLIER * 4 + min(40, trend.mentions_count * 2)), 1)
        competition = round(trend.saturation_score, 1)
        urgency = round(min(100, trend.momentum * 2.5), 1)
        viability = round(min(100, 40 + (20 if trend.source_count >= 2 else 0) + profile["viability_bonus"]), 1)
        potential = round(trend.trend_score, 1)

        if competition < 35:
            competition_label = "Low -- open gap"
        elif competition < 65:
            competition_label = "Moderate"
        else:
            competition_label = "High -- crowded space"

        if trend.momentum >= 25:
            velocity_label = "Accelerating fast"
        elif trend.momentum >= 10:
            velocity_label = "Growing"
        else:
            velocity_label = "Stable / early signal"

        if trend.mentions_count >= 5 or trend.engagement_count >= 500:
            market_size_label = (
                f"Visible traction -- {trend.source_count} source(s), {trend.mentions_count} mention(s)"
            )
        else:
            market_size_label = "Emerging signal -- still few mentions, validate before committing resources"

        risks = []
        if competition >= 65:
            risks.append("Already a crowded space: real differentiation needed before building")
        if trend.source_count <= 1:
            risks.append("Single-source signal -- validate with additional data before investing")
        if trend.category == "emerging":
            risks.append("Category not defined yet: real demand is still unconfirmed")
        if not risks:
            risks.append("No elevated risk signals detected in the current data")

        mvp_recommendation = (
            trend.saas_opportunities[0]
            if trend.saas_opportunities
            else f"Build a focused tool around {trend.title.lower()}"
        )

        return {
            "executive_summary": trend.ai_insights,
            "why_now": f"{velocity_label} -- momentum of {trend.momentum} in the latest signal.",
            "icp": profile["icp"],
            "problem": profile["problem"],
            "competition_level": competition_label,
            "mvp_recommendation": mvp_recommendation,
            "monetization_models": profile["monetization_models"],
            "risks": risks,
            "market_velocity": velocity_label,
            "market_size_signal": market_size_label,
            "scores": {
                "market": market,
                "competition": competition,
                "urgency": urgency,
                "viability": viability,
                "potential": potential,
            },
        }
