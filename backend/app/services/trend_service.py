"""Business logic for trends."""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from sqlalchemy import or_
from sqlalchemy.orm import Session, selectinload

from app.models.base import Trend, TrendSource
from app.schemas.schemas import TrendCreate


class TrendService:
    """Application service for trend use cases."""

    def __init__(self, db: Session):
        self.db = db

    def list_trends(
        self,
        q: str | None = None,
        category: str | None = None,
        source_type: str | None = None,
        min_score: float = 0,
        limit: int = 20,
        skip: int = 0,
    ) -> list[Trend]:
        query = self.db.query(Trend).options(selectinload(Trend.sources)).filter(
            Trend.is_active.is_(True),
            Trend.trend_score >= min_score,
        )

        if category:
            query = query.filter(Trend.category == category)

        if source_type:
            query = query.filter(Trend.sources.any(TrendSource.source_type == source_type))

        if q:
            search = f"%{q.lower()}%"
            query = query.filter(
                or_(
                    Trend.title.ilike(search),
                    Trend.description.ilike(search),
                    Trend.content_summary.ilike(search),
                )
            )

        return query.order_by(Trend.trend_score.desc(), Trend.detected_at.desc()).offset(skip).limit(limit).all()

    def get_trend(self, trend_id_or_slug: str) -> Trend | None:
        return (
            self.db.query(Trend)
            .options(selectinload(Trend.sources))
            .filter(
                Trend.is_active.is_(True),
                or_(Trend.id == trend_id_or_slug, Trend.slug == trend_id_or_slug),
            )
            .first()
        )

    def create_trend(self, payload: TrendCreate) -> Trend:
        existing = self.db.query(Trend).filter(Trend.slug == payload.slug).first()
        if existing:
            return existing

        trend = Trend(
            id=str(uuid4()),
            title=payload.title,
            slug=payload.slug,
            description=payload.description,
            category=payload.category,
            keywords=payload.keywords or [],
            tags=payload.tags or [],
            trend_score=50.0,
            opportunity_score=50.0,
            saturation_score=20.0,
            momentum=10.0,
            content_summary=payload.description,
            ai_insights="Manual MVP trend. Run the analyzer agent later to enrich this.",
            detected_at=datetime.now(timezone.utc).replace(tzinfo=None),
            expires_at=datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=90),
        )
        self.db.add(trend)
        self.db.commit()
        self.db.refresh(trend)
        return trend

    def list_categories(self) -> list[str]:
        rows = (
            self.db.query(Trend.category)
            .filter(Trend.is_active.is_(True))
            .distinct()
            .order_by(Trend.category.asc())
            .all()
        )
        return [row[0] for row in rows]

    def list_sources(self) -> list[str]:
        rows = (
            self.db.query(TrendSource.source_type)
            .join(Trend, Trend.id == TrendSource.trend_id)
            .filter(Trend.is_active.is_(True))
            .distinct()
            .order_by(TrendSource.source_type.asc())
            .all()
        )
        return [row[0] for row in rows]

    def best_opportunity(self) -> Trend | None:
        """The single highest-scored active trend -- the dashboard's hero card.

        Prefers trends that already have a computed opportunity_brief (real
        ingested signal) over older/seed rows that predate it, so the hero
        card is never empty-looking even right after a fresh deploy.
        """
        base_query = (
            self.db.query(Trend)
            .options(selectinload(Trend.sources))
            .filter(Trend.is_active.is_(True))
            .order_by(Trend.opportunity_score.desc(), Trend.trend_score.desc())
        )
        with_brief = base_query.filter(Trend.opportunity_brief.is_not(None)).first()
        return with_brief or base_query.first()

    def top_opportunities(self, limit: int = 5, exclude_ids: set[str] | None = None) -> list[Trend]:
        """Highest opportunity_score trends, for the "what should I build" list."""
        query = self.db.query(Trend).options(selectinload(Trend.sources)).filter(Trend.is_active.is_(True))
        if exclude_ids:
            query = query.filter(Trend.id.notin_(exclude_ids))
        return query.order_by(Trend.opportunity_score.desc()).limit(limit).all()

    def emerging_markets(self, limit: int = 5, exclude_ids: set[str] | None = None) -> list[Trend]:
        """Top trends grouped by category, one representative per category --
        a proxy for "which markets" rather than "which single trend"."""
        query = (
            self.db.query(Trend)
            .options(selectinload(Trend.sources))
            .filter(Trend.is_active.is_(True))
        )
        if exclude_ids:
            query = query.filter(Trend.id.notin_(exclude_ids))
        ranked = query.order_by(Trend.trend_score.desc()).all()
        seen_categories: set[str] = set()
        picks: list[Trend] = []
        for trend in ranked:
            if trend.category in seen_categories:
                continue
            seen_categories.add(trend.category)
            picks.append(trend)
            if len(picks) >= limit:
                break
        return picks

    def underserved_niches(self, limit: int = 5, exclude_ids: set[str] | None = None) -> list[Trend]:
        """Decent opportunity, low competition: real demand without a crowded field yet.

        Ranked by the gap between opportunity and saturation, not raw
        opportunity_score, so this reads as a genuinely different cut of the
        data instead of converging on the same names as top_opportunities.
        """
        query = (
            self.db.query(Trend)
            .options(selectinload(Trend.sources))
            .filter(Trend.is_active.is_(True), Trend.saturation_score < 45)
        )
        if exclude_ids:
            query = query.filter(Trend.id.notin_(exclude_ids))
        candidates = query.all()
        candidates.sort(key=lambda trend: trend.opportunity_score - trend.saturation_score, reverse=True)
        return candidates[:limit]

    def accelerating(self, limit: int = 5, exclude_ids: set[str] | None = None) -> list[Trend]:
        """Fastest-moving trends right now, regardless of overall score yet."""
        query = self.db.query(Trend).options(selectinload(Trend.sources)).filter(Trend.is_active.is_(True))
        if exclude_ids:
            query = query.filter(Trend.id.notin_(exclude_ids))
        return query.order_by(Trend.momentum.desc()).limit(limit).all()
