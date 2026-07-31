"""Retroactive content-quality cleanup for trends already in the database.

The ingestion gate in DetectorService only ever checks a signal once, when
it first arrives. When the filter itself improves (new relevance terms,
better language detection), that improvement only protects new signals --
whatever already made it through the old, weaker filter keeps sitting on
the dashboard untouched, since nothing re-checks it. Found live, three
times, before this existed: stale off-topic/non-English trends lingered
until someone happened to look for them. This module is the retroactive
half of the gate, meant to run on a schedule (see
scripts/run_scheduled_ingestion.py) instead of only when remembered.

Soft delete via is_active=False, not a hard delete -- reversible.
"""

import logging

from sqlalchemy.orm import Session

from app.models.base import Trend
from app.services.text_filters import RELEVANCE_TERMS, looks_non_english

logger = logging.getLogger(__name__)

_RELEVANCE_CHECKED_SOURCES = {"hackernews", "rss"}


def deactivate_non_english_trends(db: Session) -> list[str]:
    """Deactivate active trends whose title/description reads non-English."""
    trends = db.query(Trend).filter(Trend.is_active.is_(True)).all()
    deactivated = []
    for trend in trends:
        haystack = f"{trend.title or ''} {trend.description or ''}"
        if looks_non_english(haystack):
            trend.is_active = False
            deactivated.append(trend.title)
    db.commit()
    return deactivated


def deactivate_off_topic_trends(db: Session) -> list[str]:
    """Deactivate active HN/RSS-sourced trends with no on-topic keyword match."""
    trends = db.query(Trend).filter(Trend.is_active.is_(True)).all()
    deactivated = []
    for trend in trends:
        source_types = {source.source_type for source in trend.sources}
        if not source_types & _RELEVANCE_CHECKED_SOURCES:
            continue
        haystack = " ".join([trend.title or "", trend.description or ""]).lower()
        if not any(term in haystack for term in RELEVANCE_TERMS):
            trend.is_active = False
            deactivated.append(trend.title)
    db.commit()
    return deactivated


def run_content_quality_cleanup(db: Session) -> dict[str, list[str]]:
    """Run every retroactive cleanup pass and log what it removed."""
    non_english = deactivate_non_english_trends(db)
    off_topic = deactivate_off_topic_trends(db)
    if non_english:
        logger.info("Deactivated %s non-English trend(s): %s", len(non_english), non_english)
    if off_topic:
        logger.info("Deactivated %s off-topic trend(s): %s", len(off_topic), off_topic)
    return {"non_english": non_english, "off_topic": off_topic}
