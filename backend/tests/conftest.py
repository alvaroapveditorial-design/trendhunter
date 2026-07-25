"""Shared test fixtures."""

import pytest

from app.models.base import Base
from app.models.database import SessionLocal, engine


@pytest.fixture(autouse=True)
def reset_database():
    """Start each test against a clean database.

    Tests share a single SQLite file with no isolation otherwise, so state
    from one test's signals/trends can silently bleed into another's.
    """
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()
    finally:
        db.close()
    yield
