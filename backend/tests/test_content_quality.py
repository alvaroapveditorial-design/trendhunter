"""Tests for the retroactive content-quality cleanup pass."""

from uuid import uuid4

from app.models.base import Trend, TrendSource
from app.models.database import SessionLocal
from app.services.content_quality import (
    deactivate_non_english_trends,
    deactivate_off_topic_trends,
    run_content_quality_cleanup,
)


def _make_trend(db, *, title: str, description: str, source_type: str = "hackernews") -> Trend:
    trend = Trend(
        id=str(uuid4()),
        title=title,
        slug=f"{title.lower().replace(' ', '-')}-{uuid4().hex[:8]}",
        description=description,
        category="emerging",
        is_active=True,
    )
    db.add(trend)
    db.flush()
    db.add(
        TrendSource(
            id=str(uuid4()),
            trend_id=trend.id,
            source_type=source_type,
            source_id=str(uuid4()),
        )
    )
    db.commit()
    return trend


def test_deactivate_non_english_trends_catches_stale_pre_fix_data():
    """A trend that made it through an older, weaker language filter must
    still be caught retroactively -- this is what regressed in production:
    the filter improved but nothing re-checked what already existed."""
    db = SessionLocal()
    try:
        trend = _make_trend(
            db,
            title="Inferencex Regression",
            description="开源持续推理基准研究平台 -- Kimi K2.7-Code、MiniMax M3、DeepSeekv4",
        )
        deactivated = deactivate_non_english_trends(db)
        assert trend.title in deactivated

        db.refresh(trend)
        assert trend.is_active is False
    finally:
        db.close()


def test_deactivate_off_topic_trends_catches_stale_pre_fix_data():
    """Regression test for the real incident: 'Keychron announces first
    open-source firmware for gaming mice' passed an older filter and kept
    getting touched by later runs without ever being re-validated."""
    db = SessionLocal()
    try:
        trend = _make_trend(
            db,
            title="Keychron Announces First Open-Source Firmware",
            description="Keychron announces first open-source firmware for gaming mice",
        )
        deactivated = deactivate_off_topic_trends(db)
        assert trend.title in deactivated

        db.refresh(trend)
        assert trend.is_active is False
    finally:
        db.close()


def test_off_topic_cleanup_leaves_relevant_trends_alone():
    db = SessionLocal()
    try:
        trend = _make_trend(
            db,
            title="Ilya Sutskever Safe Superintelligence Partners",
            description="Safe Superintelligence announced a partnership with Nvidia.",
        )
        deactivated = deactivate_off_topic_trends(db)
        assert trend.title not in deactivated

        db.refresh(trend)
        assert trend.is_active is True
    finally:
        db.close()


def test_off_topic_cleanup_ignores_github_sourced_trends():
    """GitHub signals are pre-scoped by the search query (topic:ai) -- the
    relevance keyword gate only applies to HN/RSS, which pull from broad,
    general-purpose feeds."""
    db = SessionLocal()
    try:
        trend = _make_trend(
            db,
            title="Totally Unrelated Repo Name",
            description="A repository with a description containing no relevance keywords at all.",
            source_type="github",
        )
        deactivated = deactivate_off_topic_trends(db)
        assert trend.title not in deactivated
    finally:
        db.close()


def test_run_content_quality_cleanup_runs_both_passes():
    db = SessionLocal()
    try:
        non_english = _make_trend(
            db, title="Chinese Regression Two", description="开源持续推理基准研究平台"
        )
        off_topic = _make_trend(
            db,
            title="Off Topic Regression Two",
            description="A pub in London that is equidistant from three tube stations.",
        )

        result = run_content_quality_cleanup(db)

        assert non_english.title in result["non_english"]
        assert off_topic.title in result["off_topic"]
    finally:
        db.close()
