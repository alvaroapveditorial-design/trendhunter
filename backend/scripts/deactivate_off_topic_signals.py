"""One-off cleanup: deactivate HN/RSS-sourced trends ingested before the
relevance filter existed -- general news/science/culture stories that
happened to make HN's front page or a startup-news feed, with nothing to do
with SaaS or software (e.g. "Hannah Fry Wins Leelavati Prize").

Soft delete via is_active=False, not a hard delete -- reversible.
"""

import logging

from app.models.base import Trend
from app.models.database import SessionLocal
from app.services.hackernews_collector import RELEVANCE_TERMS
from app.services.rss_collector import RELEVANCE_TERMS as RSS_RELEVANCE_TERMS

logging.basicConfig(level="INFO")
logger = logging.getLogger("deactivate_off_topic_signals")

ALL_RELEVANCE_TERMS = RELEVANCE_TERMS | RSS_RELEVANCE_TERMS


def main() -> None:
    db = SessionLocal()
    try:
        trends = db.query(Trend).filter(Trend.is_active.is_(True)).all()
        deactivated = []
        for trend in trends:
            source_types = {source.source_type for source in trend.sources}
            if not source_types & {"hackernews", "rss"}:
                continue
            haystack = " ".join([trend.title or "", trend.description or ""]).lower()
            if not any(term in haystack for term in ALL_RELEVANCE_TERMS):
                trend.is_active = False
                deactivated.append(trend.title)
        db.commit()
        logger.info("Deactivated %s trend(s): %s", len(deactivated), deactivated)
    finally:
        db.close()


if __name__ == "__main__":
    main()
