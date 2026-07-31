"""Standalone entrypoint for scheduled ingestion (Railway cron).

Runs the same collect-then-detect pipeline as the protected HTTP ingestion
endpoints, but in-process against the database directly: no network round
trip or shared secret needed since this runs inside the trusted backend
image, just on its own cron schedule instead of serving HTTP traffic.
"""

import logging
from typing import Callable

from app.core.config import get_settings
from app.models.database import SessionLocal
from app.schemas.schemas import SignalBatchIngest, SignalIngest
from app.services.content_quality import run_content_quality_cleanup
from app.services.detector_service import DetectorService
from app.services.github_collector import GitHubCollector
from app.services.hackernews_collector import HackerNewsCollector
from app.services.rss_collector import RSSCollector

logging.basicConfig(level="INFO")
logger = logging.getLogger("scheduled_ingestion")

_settings = get_settings()
if _settings.SENTRY_DSN:
    import sentry_sdk

    sentry_sdk.init(dsn=_settings.SENTRY_DSN, environment=_settings.ENVIRONMENT)


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
    except Exception as exc:
        logger.exception("%s: ingestion failed", name)
        if _settings.SENTRY_DSN:
            import sentry_sdk

            sentry_sdk.capture_exception(exc)
    finally:
        db.close()


def _run_cleanup() -> None:
    db = SessionLocal()
    try:
        run_content_quality_cleanup(db)
    except Exception as exc:
        logger.exception("content quality cleanup failed")
        if _settings.SENTRY_DSN:
            import sentry_sdk

            sentry_sdk.capture_exception(exc)
    finally:
        db.close()


def main() -> None:
    _run_source("github", lambda: GitHubCollector().collect(limit=15))
    _run_source("hackernews", lambda: HackerNewsCollector().collect(feed="top", limit=15))
    _run_source("rss", lambda: RSSCollector().collect(limit=10))
    # Retroactive pass: catches trends that made it through an older, weaker
    # version of the filters above, not just what today's signals produced.
    _run_cleanup()


if __name__ == "__main__":
    main()
