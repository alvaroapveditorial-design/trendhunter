"""One-off: deactivate every trend so the next ingestion run starts from a
clean slate. Used once after a scoring/sampling fix to avoid mixing old
data (computed under the previous formula/sort order) with new, correctly
computed data in the same view.

Soft delete via is_active=False, not a hard delete -- reversible.
"""

import logging

from app.models.base import Trend
from app.models.database import SessionLocal

logging.basicConfig(level="INFO")
logger = logging.getLogger("purge_and_reset_trends")


def main() -> None:
    db = SessionLocal()
    try:
        count = db.query(Trend).filter(Trend.is_active.is_(True)).update({Trend.is_active: False})
        db.commit()
        logger.info("Deactivated %s trend(s)", count)
    finally:
        db.close()


if __name__ == "__main__":
    main()
