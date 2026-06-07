"""Clean historical MVP trend data for a cleaner demo dashboard."""

from __future__ import annotations

from datetime import datetime, timezone

from app.models.base import Trend, TrendSource
from app.models.database import SessionLocal
from app.services.detector_service import DetectorService, GENERIC_TITLE_KEYWORDS, slugify
from app.schemas.schemas import SignalIngest

LOW_QUALITY_PHRASES = (
    "discussion | link",
    "my keyboard fell apart",
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _unique_slug(db, title: str, trend_id: str) -> str:
    base = slugify(title)
    slug = base
    suffix = 2
    while db.query(Trend).filter(Trend.slug == slug, Trend.id != trend_id).first():
        slug = f"{base[:72]}-{suffix}"
        suffix += 1
    return slug


def _best_source(trend: Trend) -> TrendSource | None:
    sources = list(trend.sources or [])
    if not sources:
        return None
    return max(
        sources,
        key=lambda source: (
            (source.upvotes or 0) + (source.comments or 0) * 2 + (source.shares or 0) * 3,
            source.published_at or source.fetched_at,
        ),
    )


def _clean_text(value: str | None) -> str | None:
    if not value:
        return value
    return value.replace("Discussion | Link", "").strip()


def _should_hide(trend: Trend) -> bool:
    text = " ".join(
        part.lower()
        for part in [
            trend.title,
            trend.description,
            trend.content_summary,
            " ".join(trend.keywords or []),
        ]
        if part
    )
    if any(phrase in text for phrase in LOW_QUALITY_PHRASES):
        return True
    return (trend.source_count or 0) >= 8 and len(trend.keywords or []) >= 30


def _should_retitle(title: str) -> bool:
    normalized = title.strip().lower()
    words = normalized.split()
    if normalized in GENERIC_TITLE_KEYWORDS:
        return True
    if len(words) <= 1:
        return True
    return any(word in {"get", "most", "now", "some", "want", "you", "your"} for word in words)


def clean_history() -> dict[str, int]:
    db = SessionLocal()
    detector = DetectorService(db)
    stats = {"updated": 0, "retitled": 0, "hidden": 0}

    try:
        trends = db.query(Trend).all()
        for trend in trends:
            changed = False
            trend.description = _clean_text(trend.description)
            trend.content_summary = _clean_text(trend.content_summary)

            cleaned_keywords = detector._clean_keywords_list(trend.keywords or [])
            if cleaned_keywords != (trend.keywords or []):
                trend.keywords = cleaned_keywords
                trend.tags = cleaned_keywords[:6]
                changed = True

            if trend.is_active and _should_hide(trend):
                trend.is_active = False
                stats["hidden"] += 1
                changed = True

            source = _best_source(trend)
            if trend.is_active and source and _should_retitle(trend.title):
                signal = SignalIngest(
                    title=source.title or trend.title,
                    content=source.content or trend.description,
                    source_type=source.source_type,
                    source_url=source.source_url,
                    source_id=source.source_id,
                    upvotes=source.upvotes or 0,
                    comments=source.comments or 0,
                    shares=source.shares or 0,
                    keywords=cleaned_keywords,
                    category=trend.category,
                    published_at=source.published_at,
                )
                new_title = detector._trend_title(signal, cleaned_keywords)
                if new_title and new_title != trend.title:
                    trend.title = new_title
                    trend.slug = _unique_slug(db, new_title, trend.id)
                    stats["retitled"] += 1
                    changed = True

            if changed:
                trend.last_updated_at = _utcnow()
                stats["updated"] += 1

        active_by_title: dict[str, list[Trend]] = {}
        for trend in db.query(Trend).filter(Trend.is_active.is_(True)).all():
            active_by_title.setdefault(trend.title.strip().lower(), []).append(trend)

        for duplicates in active_by_title.values():
            if len(duplicates) <= 1:
                continue
            keep = max(
                duplicates,
                key=lambda trend: (
                    trend.trend_score or 0,
                    trend.source_count or 0,
                    trend.last_updated_at or trend.detected_at,
                ),
            )
            for trend in duplicates:
                if trend.id == keep.id:
                    continue
                trend.is_active = False
                trend.last_updated_at = _utcnow()
                stats["hidden"] += 1
                stats["updated"] += 1

        db.commit()
        return stats
    finally:
        db.close()


if __name__ == "__main__":
    result = clean_history()
    print(
        "Cleaned trend history: "
        f"{result['updated']} updated, {result['retitled']} retitled, {result['hidden']} hidden"
    )
