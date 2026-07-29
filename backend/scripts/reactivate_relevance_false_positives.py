"""One-off: reactivate trends wrongly deactivated by deactivate_off_topic_signals.py
before RELEVANCE_TERMS was expanded to cover AI model/company/technique names
(e.g. "Ilya Sutskever ... Safe Superintelligence", "Kimi K3", "PyTorch").

Soft undo of a soft delete -- reversible, matches the original script's
approach (is_active flip, not a hard delete).
"""

import logging

from app.models.base import Trend
from app.models.database import SessionLocal

logging.basicConfig(level="INFO")
logger = logging.getLogger("reactivate_relevance_false_positives")

TITLES_TO_REACTIVATE = {
    "Benchmarking Opus Slopcodebench",
    "Codex Security",
    "Cursor Makes Its Biggest India",
    "Ilya Sutskever Safe Superintelligence Partners",
    "Kimi K3 Architecture Overview Notes",
    "Open Model Feels Surprisingly Good",
    "Position Open-Weights Models",
    "Pytorch Reference Language",
    "Rl Fine-Tune Open Model Beat",
    "Transformer Transformer Unified Model Motion-Conditioned",
}


def main() -> None:
    db = SessionLocal()
    try:
        trends = db.query(Trend).filter(Trend.title.in_(TITLES_TO_REACTIVATE)).all()
        reactivated = []
        for trend in trends:
            trend.is_active = True
            reactivated.append(trend.title)
        db.commit()
        logger.info("Reactivated %s trend(s): %s", len(reactivated), reactivated)
        missing = TITLES_TO_REACTIVATE - set(reactivated)
        if missing:
            logger.warning("Not found: %s", missing)
    finally:
        db.close()


if __name__ == "__main__":
    main()
