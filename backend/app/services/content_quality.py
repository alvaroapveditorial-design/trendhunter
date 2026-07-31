"""Retroactive content-quality cleanup for trends already in the database.

The ingestion gate in DetectorService only ever checks a signal once, when
it first arrives. When the filter itself improves (new relevance terms,
better language detection), that improvement only protects new signals --
whatever already made it through the old, weaker filter keeps sitting on
the dashboard untouched, since nothing re-checks it. Found live, three
times, before this existed: stale off-topic/non-English trends lingered
until someone happened to look for them. This module is the retroactive
half of the gate, run on a schedule (see scripts/run_scheduled_ingestion.py)
instead of only when remembered.

Soft delete via is_active=False, not a hard delete -- reversible. Each pass
queries and commits independently, so a failure in one never blocks or
half-applies the other -- every commit is a fully consistent state on its
own, and re-running finds nothing left to do (idempotent).
"""

import logging
import time
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.base import AgentExecution, Trend
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


def run_content_quality_cleanup(db: Session) -> dict:
    """Run every retroactive cleanup pass, logging a structured summary and
    an AgentExecution row -- the same audit trail the ingestion pipeline
    already uses, so this shows up in "Recent pipeline runs" next to the
    collectors instead of only existing in Railway's log stream.

    Each pass is isolated: if one raises, it's caught, rolled back, and
    recorded as an error, but the other pass still runs. A partial failure
    here never leaves is_active flags half-applied -- each pass's own
    db.commit() is the only place state changes, and that only happens on
    a clean, complete pass.
    """
    started_at = datetime.now(timezone.utc).replace(tzinfo=None)
    start_perf = time.perf_counter()
    reviewed = db.query(Trend).filter(Trend.is_active.is_(True)).count()

    execution = AgentExecution(
        id=str(uuid4()),
        agent_name="content_quality_cleanup",
        agent_type="data_hygiene",
        status="running",
        input_params={"reviewed": reviewed},
        started_at=started_at,
    )
    db.add(execution)
    db.flush()

    non_english: list[str] = []
    off_topic: list[str] = []
    errors: list[str] = []

    try:
        non_english = deactivate_non_english_trends(db)
    except Exception as exc:
        logger.exception("non-English cleanup pass failed")
        db.rollback()
        db.add(execution)  # rollback expunges pending objects; re-attach it
        errors.append(f"non_english: {exc}")

    try:
        off_topic = deactivate_off_topic_trends(db)
    except Exception as exc:
        logger.exception("off-topic cleanup pass failed")
        db.rollback()
        db.add(execution)  # rollback expunges pending objects; re-attach it
        errors.append(f"off_topic: {exc}")

    completed_at = datetime.now(timezone.utc).replace(tzinfo=None)
    duration_seconds = round(time.perf_counter() - start_perf, 3)
    deactivated_total = len(non_english) + len(off_topic)

    execution.status = "failed" if errors else "success"
    execution.completed_at = completed_at
    execution.duration_seconds = duration_seconds
    execution.records_processed = reviewed
    execution.records_updated = deactivated_total
    execution.error_message = "; ".join(errors) if errors else None
    execution.output = {
        "non_english_deactivated": non_english,
        "off_topic_deactivated": off_topic,
        "errors": errors,
    }
    db.commit()

    logger.info(
        "content_quality_cleanup started_at=%s completed_at=%s duration_seconds=%s "
        "reviewed=%s deactivated=%s (non_english=%s off_topic=%s) errors=%s",
        started_at.isoformat(),
        completed_at.isoformat(),
        duration_seconds,
        reviewed,
        deactivated_total,
        len(non_english),
        len(off_topic),
        len(errors),
    )

    return {
        "started_at": started_at,
        "completed_at": completed_at,
        "duration_seconds": duration_seconds,
        "reviewed": reviewed,
        "deactivated_total": deactivated_total,
        "non_english": non_english,
        "off_topic": off_topic,
        "errors": errors,
    }
