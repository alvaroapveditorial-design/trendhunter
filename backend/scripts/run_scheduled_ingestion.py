"""Standalone entrypoint for scheduled ingestion (Railway cron).

Runs the same collect-then-detect pipeline as the protected HTTP ingestion
endpoints, but in-process against the database directly: no network round
trip or shared secret needed since this runs inside the trusted backend
image, just on its own cron schedule instead of serving HTTP traffic.
"""

import logging
from typing import Callable

from app.models.database import SessionLocal
from app.schemas.schemas import SignalBatchIngest, SignalIngest
from app.services.detector_service import DetectorService
from app.services.github_collector import GitHubCollector
from app.services.hackernews_collector import HackerNewsCollector
from app.services.rss_collector import RSSCollector

logging.basicConfig(level="INFO")
logger = logging.getLogger("scheduled_ingestion")


def _run_source(name: str, collect: Callable[[], list[SignalIngest]]) -> None:
    db = SessionLocal()
    try:
        signals = collect()
        if not signals:
            logger.info("%s: no signals collected", name)
            return
        result = DetectorService(db).ingest_batch(SignalBatchIngest(signals=signals))
        logger.info(
            "%s: processed=%s created=%s updated=%s",
            name,
            len(signals),
            result.created_trends,
            result.updated_trends,
        )
    except Exception:
        logger.exception("%s: ingestion failed", name)
    finally:
        db.close()


def main() -> None:
    _run_source("github", lambda: GitHubCollector().collect(limit=15))
    _run_source("hackernews", lambda: HackerNewsCollector().collect(feed="top", limit=15))
    _run_source("rss", lambda: RSSCollector().collect(limit=10))


if __name__ == "__main__":
    main()
