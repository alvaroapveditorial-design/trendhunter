"""Tests for the retroactive content-quality cleanup pass."""

from uuid import uuid4

from app.models.base import AgentExecution, Trend, TrendSource
from app.models.database import SessionLocal
from app.services import content_quality
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


def test_run_content_quality_cleanup_records_agent_execution():
    """The cleanup must be visible in the same audit trail the ingestion
    pipeline already uses (agent_executions -> "Recent pipeline runs" on
    the dashboard), with the fields the CTO/CPO decision asked for: start
    time, end time, reviewed count, deactivated count, duration, errors."""
    db = SessionLocal()
    try:
        _make_trend(db, title="Audit Trail Regression", description="开源持续推理基准研究平台")

        result = run_content_quality_cleanup(db)

        execution = (
            db.query(AgentExecution)
            .filter(AgentExecution.agent_name == "content_quality_cleanup")
            .order_by(AgentExecution.started_at.desc())
            .first()
        )
        assert execution is not None
        assert execution.status == "success"
        assert execution.started_at is not None
        assert execution.completed_at is not None
        assert execution.duration_seconds is not None
        assert execution.records_processed == result["reviewed"]
        assert execution.records_updated == result["deactivated_total"]
        assert execution.error_message is None
        assert execution.output["non_english_deactivated"]
    finally:
        db.close()


def test_run_content_quality_cleanup_is_idempotent():
    """Running the cleanup twice in a row must not error, must not touch
    already-deactivated trends again, and the second run should find
    nothing left to do."""
    db = SessionLocal()
    try:
        trend = _make_trend(
            db, title="Idempotency Regression", description="开源持续推理基准研究平台"
        )

        first = run_content_quality_cleanup(db)
        assert trend.title in first["non_english"]

        second = run_content_quality_cleanup(db)
        assert trend.title not in second["non_english"]
        assert trend.title not in second["off_topic"]
    finally:
        db.close()


def test_run_content_quality_cleanup_one_pass_failing_does_not_block_the_other(monkeypatch):
    """A failure in one pass must be caught, rolled back, and recorded --
    but must not prevent the other pass from running, and must not leave
    is_active flags half-applied."""
    db = SessionLocal()
    try:
        non_english_trend = _make_trend(
            db, title="Failure Isolation Non-English", description="开源持续推理基准研究平台"
        )
        off_topic_trend = _make_trend(
            db,
            title="Off Topic Isolation Check",
            description="A pub in London that is equidistant from three tube stations.",
        )

        def boom(_db):
            raise RuntimeError("simulated failure")

        monkeypatch.setattr(content_quality, "deactivate_non_english_trends", boom)

        result = run_content_quality_cleanup(db)

        assert result["errors"]
        assert off_topic_trend.title in result["off_topic"]

        execution = (
            db.query(AgentExecution)
            .filter(AgentExecution.agent_name == "content_quality_cleanup")
            .order_by(AgentExecution.started_at.desc())
            .first()
        )
        assert execution.status == "failed"
        assert "simulated failure" in execution.error_message

        db.refresh(non_english_trend)
        db.refresh(off_topic_trend)
        assert non_english_trend.is_active is True
        assert off_topic_trend.is_active is False
    finally:
        db.close()
