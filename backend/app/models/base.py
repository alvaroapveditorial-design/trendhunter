"""Database models for SQLAlchemy ORM."""

from datetime import datetime, timezone


def _utcnow() -> datetime:
    """Return current UTC time as a naive datetime (SQLAlchemy compatible)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)
from typing import Optional

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    """User account model."""

    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)

    # Account status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    # Subscription
    subscription_plan = Column(String, default="free")  # free, pro, enterprise
    subscription_started_at = Column(DateTime, nullable=True)
    subscription_ends_at = Column(DateTime, nullable=True)
    stripe_customer_id = Column(String, nullable=True, index=True)

    # Timestamps
    created_at = Column(DateTime, default=_utcnow, index=True)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)
    last_login_at = Column(DateTime, nullable=True)

    # Relationships
    alerts = relationship("Alert", back_populates="user", cascade="all, delete-orphan")
    saved_trends = relationship("SavedTrend", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (Index("idx_user_email", "email"),)


class Trend(Base):
    """Detected trend model."""

    __tablename__ = "trends"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)

    # Scoring
    trend_score = Column(Float, default=0.0, index=True)  # 0-100
    opportunity_score = Column(Float, default=0.0)  # 0-100
    saturation_score = Column(Float, default=0.0)  # 0-100
    momentum = Column(Float, default=0.0)  # growth rate

    # Classification
    category = Column(String, index=True, nullable=False)  # e.g., "ai_ml", "saas"
    tags = Column(JSON, default=[])  # list of tags
    keywords = Column(JSON, default=[])  # related keywords

    # Content
    content_summary = Column(Text, nullable=True)
    ai_insights = Column(Text, nullable=True)
    saas_opportunities = Column(JSON, default=[])

    # Statistics
    mentions_count = Column(Integer, default=0)
    engagement_count = Column(Integer, default=0)
    source_count = Column(Integer, default=0)

    # Tracking
    detected_at = Column(DateTime, default=_utcnow, index=True)
    last_updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)
    peak_at = Column(DateTime, nullable=True)  # when trend peaked
    expires_at = Column(DateTime, nullable=True, index=True)

    # Status
    is_active = Column(Boolean, default=True, index=True)
    is_verified = Column(Boolean, default=False)

    # Relationships
    sources = relationship("TrendSource", back_populates="trend", cascade="all, delete-orphan")
    embeddings = relationship("TrendEmbedding", back_populates="trend", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_trend_score_active", "trend_score", "is_active"),
        Index("idx_trend_category_active", "category", "is_active"),
    )


class TrendSource(Base):
    """Source data for a trend."""

    __tablename__ = "trend_sources"

    id = Column(String, primary_key=True, index=True)
    trend_id = Column(String, ForeignKey("trends.id"), index=True, nullable=False)
    source_type = Column(String, index=True, nullable=False)  # reddit, github, hackernews, etc.
    source_url = Column(String, nullable=True)
    source_id = Column(String, nullable=True, index=True)  # source-specific ID

    # Content
    title = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    author = Column(String, nullable=True)

    # Metrics
    upvotes = Column(Integer, default=0)
    downvotes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)

    # Metadata
    published_at = Column(DateTime, nullable=True)
    fetched_at = Column(DateTime, default=_utcnow)

    # Relationships
    trend = relationship("Trend", back_populates="sources")

    __table_args__ = (
        UniqueConstraint("trend_id", "source_type", "source_id", name="uq_trend_source"),
        Index("idx_source_type", "source_type"),
    )


class TrendEmbedding(Base):
    """Vector embedding for trend similarity search."""

    __tablename__ = "trend_embeddings"

    id = Column(String, primary_key=True, index=True)
    trend_id = Column(String, ForeignKey("trends.id"), index=True, nullable=False)
    embedding = Column(JSON, nullable=False)  # Vector embedding
    embedding_model = Column(String, default="text-embedding-3-small")
    created_at = Column(DateTime, default=_utcnow)

    # Relationships
    trend = relationship("Trend", back_populates="embeddings")


class Alert(Base):
    """User alert configuration."""

    __tablename__ = "alerts"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)

    # Alert config
    name = Column(String, nullable=False)
    keywords = Column(JSON, nullable=False)  # list of keywords to watch
    categories = Column(JSON, default=[])  # filter by category
    min_score = Column(Float, default=50.0)  # minimum trend score

    # Notification settings
    is_active = Column(Boolean, default=True)
    notification_channel = Column(String, default="email")  # email, slack, webhook
    notify_frequency = Column(String, default="instant")  # instant, daily, weekly

    # Timestamps
    created_at = Column(DateTime, default=_utcnow)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)
    last_triggered_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="alerts")

    __table_args__ = (Index("idx_alert_user_active", "user_id", "is_active"),)


class SavedTrend(Base):
    """User saved trends."""

    __tablename__ = "saved_trends"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    trend_id = Column(String, ForeignKey("trends.id"), index=True, nullable=False)

    # Metadata
    saved_at = Column(DateTime, default=_utcnow, index=True)
    notes = Column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="saved_trends")

    __table_args__ = (UniqueConstraint("user_id", "trend_id", name="uq_user_saved_trend"),)


class AgentExecution(Base):
    """AI agent execution log."""

    __tablename__ = "agent_executions"

    id = Column(String, primary_key=True, index=True)
    agent_name = Column(String, index=True, nullable=False)
    agent_type = Column(String, nullable=False)  # source_collector, analyzer, etc.

    # Execution details
    status = Column(String, default="pending", index=True)  # pending, running, success, failed
    input_params = Column(JSON, nullable=True)
    output = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)

    # Execution time
    started_at = Column(DateTime, default=_utcnow)
    completed_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Float, nullable=True)

    # Results
    records_processed = Column(Integer, default=0)
    records_created = Column(Integer, default=0)
    records_updated = Column(Integer, default=0)

    # Relationships to created trends
    created_trend_ids = Column(JSON, default=[])  # trend IDs created by this execution

    __table_args__ = (
        Index("idx_agent_name_status", "agent_name", "status"),
        Index("idx_agent_completed", "completed_at"),
    )


class Report(Base):
    """Generated reports."""

    __tablename__ = "reports"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)

    # Report details
    title = Column(String, nullable=False)
    report_type = Column(String, nullable=False)  # weekly, custom, etc.
    format = Column(String, default="json")  # json, pdf, html

    # Content
    content = Column(JSON, nullable=True)  # JSON data for report
    pdf_url = Column(String, nullable=True)

    # Status
    status = Column(String, default="pending")  # pending, generating, completed, failed
    is_public = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime, default=_utcnow)
    completed_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)

    __table_args__ = (
        Index("idx_report_user_created", "user_id", "created_at"),
        Index("idx_report_status", "status"),
    )
