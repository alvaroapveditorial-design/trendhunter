"""One-off cleanup: deactivate trends ingested before the non-English filter
existed -- e.g. a repo with a Chinese-language description ("Lanhu Mcp").
There's no translation step in this product, so a non-English description
just looks broken to an English-only audience.

Soft delete via is_active=False, not a hard delete -- reversible.
"""

import logging

from app.models.base import Trend
from app.models.database import SessionLocal
from app.services.text_filters import looks_non_english

logging.basicConfig(level="INFO")
logger = logging.getLogger("deactivate_non_english_signals")


def main() -> None:
    db = SessionLocal()
    try:
        trends = db.query(Trend).filter(Trend.is_active.is_(True)).all()
        deactivated = []
        for trend in trends:
            haystack = f"{trend.title or ''} {trend.description or ''}"
            if looks_non_english(haystack):
                trend.is_active = False
                deactivated.append(trend.title)
        db.commit()
        logger.info("Deactivated %s trend(s): %s", len(deactivated), deactivated)
    finally:
        db.close()


if __name__ == "__main__":
    main()
