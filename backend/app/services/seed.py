"""Seed data for local MVP development."""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app.models.base import Trend, TrendSource
from app.models.database import SessionLocal


SEED_TRENDS = [
    {
        "title": "AI copilots for vertical SaaS",
        "slug": "ai-copilots-vertical-saas",
        "description": "Specialized copilots embedded inside niche business workflows.",
        "category": "ai_saas",
        "tags": ["ai", "saas", "workflow"],
        "keywords": ["copilot", "vertical SaaS", "automation"],
        "trend_score": 86.0,
        "opportunity_score": 91.0,
        "saturation_score": 43.0,
        "momentum": 31.5,
        "mentions_count": 184,
        "engagement_count": 3210,
        "source_count": 3,
        "content_summary": "Teams want AI inside the tools they already use, not another generic chatbot.",
        "ai_insights": "Best early niches have repetitive expert workflows and measurable time savings.",
        "saas_opportunities": [
            "Copilot for small legal intake teams",
            "AI workflow assistant for property managers",
            "Finance ops reconciliation assistant",
        ],
    },
    {
        "title": "Privacy-first analytics for indie products",
        "slug": "privacy-first-analytics-indie-products",
        "description": "Lightweight product analytics without invasive tracking or cookie banners.",
        "category": "privacy",
        "tags": ["privacy", "analytics", "indie-hackers"],
        "keywords": ["GDPR", "analytics", "product analytics"],
        "trend_score": 74.0,
        "opportunity_score": 78.0,
        "saturation_score": 58.0,
        "momentum": 18.2,
        "mentions_count": 92,
        "engagement_count": 870,
        "source_count": 2,
        "content_summary": "Founders want useful funnels and retention metrics with minimal compliance burden.",
        "ai_insights": "A focused analytics layer for micro-SaaS could win by being simpler than enterprise tools.",
        "saas_opportunities": [
            "GDPR-friendly onboarding analytics",
            "Simple cohort dashboards for small SaaS",
        ],
    },
    {
        "title": "Synthetic user research",
        "slug": "synthetic-user-research",
        "description": "Using AI personas to pre-test landing pages, product messaging, and feature ideas.",
        "category": "product",
        "tags": ["research", "ai", "product"],
        "keywords": ["user research", "personas", "message testing"],
        "trend_score": 69.0,
        "opportunity_score": 73.0,
        "saturation_score": 36.0,
        "momentum": 22.4,
        "mentions_count": 76,
        "engagement_count": 640,
        "source_count": 2,
        "content_summary": "Teams are using LLMs to get rough qualitative feedback before real interviews.",
        "ai_insights": "This should be positioned as pre-research, not a replacement for real users.",
        "saas_opportunities": [
            "Landing page critique for B2B founders",
            "Persona-based positioning tests",
        ],
    },
]


def seed_database() -> None:
    """Insert useful starter trends if the database is empty."""
    db = SessionLocal()
    try:
        existing_count = db.query(Trend).count()
        if existing_count:
            return

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        for index, item in enumerate(SEED_TRENDS):
            trend = Trend(
                id=str(uuid4()),
                detected_at=now - timedelta(days=index + 1),
                last_updated_at=now,
                expires_at=now + timedelta(days=90),
                is_active=True,
                is_verified=index == 0,
                **item,
            )
            db.add(trend)
            db.flush()
            db.add(
                TrendSource(
                    id=str(uuid4()),
                    trend_id=trend.id,
                    source_type="mock",
                    source_url="https://example.com/trend-signal",
                    source_id=trend.slug,
                    title=f"Seed signal: {trend.title}",
                    content=trend.content_summary,
                    upvotes=max(10, int(trend.engagement_count / 25)),
                    comments=max(1, int(trend.mentions_count / 8)),
                    published_at=trend.detected_at,
                )
            )

        db.commit()
    finally:
        db.close()
