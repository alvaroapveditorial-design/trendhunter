"""Manual one-off run of the non-English cleanup pass.

This now runs automatically every day as part of scheduled ingestion (see
run_scheduled_ingestion.py); this script is kept for on-demand manual runs
(e.g. right after widening the language filter, to clean up immediately
instead of waiting for tomorrow's cron).
"""

import logging

from app.models.database import SessionLocal
from app.services.content_quality import deactivate_non_english_trends

logging.basicConfig(level="INFO")
logger = logging.getLogger("deactivate_non_english_signals")


def main() -> None:
    db = SessionLocal()
    try:
        deactivated = deactivate_non_english_trends(db)
        logger.info("Deactivated %s trend(s): %s", len(deactivated), deactivated)
    finally:
        db.close()


if __name__ == "__main__":
    main()
