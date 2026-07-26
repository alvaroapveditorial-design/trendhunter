"""One-off backfill: compute opportunity_brief for trends ingested before it existed.

Safe to re-run: only touches rows where opportunity_brief is still NULL, using
the exact same heuristic detector_service.py computes on every new signal.
"""

import logging

from app.models.base import Trend
from app.models.database import SessionLocal
from app.services.detector_service import DetectorService

logging.basicConfig(level="INFO")
logger = logging.getLogger("backfill_opportunity_briefs")


def main() -> None:
    db = SessionLocal()
    try:
        detector = DetectorService(db)
        trends = db.query(Trend).filter(Trend.is_active.is_(True), Trend.opportunity_brief.is_(None)).all()
        logger.info("Backfilling opportunity_brief for %s trend(s)", len(trends))
        for trend in trends:
            trend.opportunity_brief = detector._build_opportunity_brief(trend)
        db.commit()
        logger.info("Done")
    finally:
        db.close()


if __name__ == "__main__":
    main()
