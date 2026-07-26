"""One-off cleanup: deactivate trends ingested before the reference-content
filter existed (interview guides, awesome-lists, course material that
matched topic:ai but were never real SaaS opportunities).

Soft delete via is_active=False, not a hard delete -- reversible, and
consistent with how the rest of the app already treats inactive trends.
"""

import logging

from app.models.base import Trend
from app.models.database import SessionLocal
from app.services.github_collector import NON_PRODUCT_MARKERS

logging.basicConfig(level="INFO")
logger = logging.getLogger("deactivate_reference_content")


def main() -> None:
    db = SessionLocal()
    try:
        trends = db.query(Trend).filter(Trend.is_active.is_(True)).all()
        deactivated = []
        for trend in trends:
            haystack = " ".join(
                [
                    trend.title or "",
                    trend.description or "",
                    " ".join(trend.keywords or []),
                ]
            ).lower()
            if any(marker in haystack for marker in NON_PRODUCT_MARKERS):
                trend.is_active = False
                deactivated.append(trend.title)
        db.commit()
        logger.info("Deactivated %s trend(s): %s", len(deactivated), deactivated)
    finally:
        db.close()


if __name__ == "__main__":
    main()
