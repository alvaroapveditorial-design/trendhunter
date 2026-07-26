"""One-off cleanup: deactivate GitHub-sourced trends ingested before the
stars:50..3000 ceiling existed, whose repo already has more stars than that
cap -- e.g. AutoGPT, Dify, ComfyUI. Already-mainstream projects are the
opposite of a hidden opportunity, so they shouldn't be sitting in the hero
slot or the top-5 lists just because they were ingested before the filter.

Soft delete via is_active=False, not a hard delete -- reversible.
"""

import logging

from app.models.base import Trend, TrendSource
from app.models.database import SessionLocal

logging.basicConfig(level="INFO")
logger = logging.getLogger("deactivate_oversized_repos")

STAR_CEILING = 3000


def main() -> None:
    db = SessionLocal()
    try:
        trends = db.query(Trend).filter(Trend.is_active.is_(True)).all()
        deactivated = []
        for trend in trends:
            github_sources = [s for s in trend.sources if s.source_type == "github"]
            if not github_sources:
                continue
            if any(source.upvotes > STAR_CEILING for source in github_sources):
                trend.is_active = False
                deactivated.append((trend.title, max(s.upvotes for s in github_sources)))
        db.commit()
        logger.info("Deactivated %s trend(s): %s", len(deactivated), deactivated)
    finally:
        db.close()


if __name__ == "__main__":
    main()
