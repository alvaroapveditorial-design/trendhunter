"""Business logic for trends."""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

from sqlalchemy import or_
from sqlalchemy.orm import Session, selectinload

from app.models.base import Trend
from app.schemas.schemas import TrendCreate


class TrendService:
    """Application service for trend use cases."""

    def __init__(self, db: Session):
        self.db = db

    def list_trends(
        self,
        q: str | None = None,
        category: str | None = None,
        min_score: float = 0,
        limit: int = 20,
        skip: int = 0,
    ) -> list[Trend]:
        query = self.db.query(Trend).filter(
            Trend.is_active.is_(True),
            Trend.trend_score >= min_score,
        )

        if category:
            query = query.filter(Trend.category == category)

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
