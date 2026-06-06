"""Initial MVP schema.

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-06-02
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column("hashed_password", sa.String(), nullable=True),
        sa.Column("avatar_url", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("is_verified", sa.Boolean(), nullable=True),
        sa.Column("is_admin", sa.Boolean(), nullable=True),
        sa.Column("subscription_plan", sa.String(), nullable=True),
        sa.Column("subscription_started_at", sa.DateTime(), nullable=True),
        sa.Column("subscription_ends_at", sa.DateTime(), nullable=True),
        sa.Column("stripe_customer_id", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("last_login_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_user_email", "users", ["email"])
    op.create_index(op.f("ix_users_created_at"), "users", ["created_at"])
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"])
    op.create_index(op.f("ix_users_stripe_customer_id"), "users", ["stripe_customer_id"])
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)

    op.create_table(
        "trends",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("trend_score", sa.Float(), nullable=True),
        sa.Column("opportunity_score", sa.Float(), nullable=True),
        sa.Column("saturation_score", sa.Float(), nullable=True),
        sa.Column("momentum", sa.Float(), nullable=True),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("tags", sa.JSON(), nullable=True),
        sa.Column("keywords", sa.JSON(), nullable=True),
        sa.Column("content_summary", sa.Text(), nullable=True),
        sa.Column("ai_insights", sa.Text(), nullable=True),
        sa.Column("saas_opportunities", sa.JSON(), nullable=True),
        sa.Column("mentions_count", sa.Integer(), nullable=True),
        sa.Column("engagement_count", sa.Integer(), nullable=True),
        sa.Column("source_count", sa.Integer(), nullable=True),
        sa.Column("detected_at", sa.DateTime(), nullable=True),
        sa.Column("last_updated_at", sa.DateTime(), nullable=True),
        sa.Column("peak_at", sa.DateTime(), nullable=True),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("is_verified", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_trend_category_active", "trends", ["category", "is_active"])
    op.create_index("idx_trend_score_active", "trends", ["trend_score", "is_active"])
    op.create_index(op.f("ix_trends_category"), "trends", ["category"])
    op.create_index(op.f("ix_trends_detected_at"), "trends", ["detected_at"])
    op.create_index(op.f("ix_trends_expires_at"), "trends", ["expires_at"])
    op.create_index(op.f("ix_trends_id"), "trends", ["id"])
    op.create_index(op.f("ix_trends_is_active"), "trends", ["is_active"])
    op.create_index(op.f("ix_trends_slug"), "trends", ["slug"], unique=True)
    op.create_index(op.f("ix_trends_title"), "trends", ["title"])
    op.create_index(op.f("ix_trends_trend_score"), "trends", ["trend_score"])

    op.create_table(
        "agent_executions",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("agent_name", sa.String(), nullable=False),
        sa.Column("agent_type", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("input_params", sa.JSON(), nullable=True),
        sa.Column("output", sa.JSON(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("duration_seconds", sa.Float(), nullable=True),
        sa.Column("records_processed", sa.Integer(), nullable=True),
        sa.Column("records_created", sa.Integer(), nullable=True),
        sa.Column("records_updated", sa.Integer(), nullable=True),
        sa.Column("created_trend_ids", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_agent_completed", "agent_executions", ["completed_at"])
    op.create_index("idx_agent_name_status", "agent_executions", ["agent_name", "status"])
    op.create_index(op.f("ix_agent_executions_agent_name"), "agent_executions", ["agent_name"])
    op.create_index(op.f("ix_agent_executions_id"), "agent_executions", ["id"])
    op.create_index(op.f("ix_agent_executions_status"), "agent_executions", ["status"])

    op.create_table(
        "alerts",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("keywords", sa.JSON(), nullable=False),
        sa.Column("categories", sa.JSON(), nullable=True),
        sa.Column("min_score", sa.Float(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("notification_channel", sa.String(), nullable=True),
        sa.Column("notify_frequency", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("last_triggered_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_alert_user_active", "alerts", ["user_id", "is_active"])
    op.create_index(op.f("ix_alerts_id"), "alerts", ["id"])
    op.create_index(op.f("ix_alerts_user_id"), "alerts", ["user_id"])

    op.create_table(
        "reports",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("report_type", sa.String(), nullable=False),
        sa.Column("format", sa.String(), nullable=True),
        sa.Column("content", sa.JSON(), nullable=True),
        sa.Column("pdf_url", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("is_public", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_report_status", "reports", ["status"])
    op.create_index("idx_report_user_created", "reports", ["user_id", "created_at"])
    op.create_index(op.f("ix_reports_id"), "reports", ["id"])
    op.create_index(op.f("ix_reports_user_id"), "reports", ["user_id"])

    op.create_table(
        "saved_trends",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("trend_id", sa.String(), nullable=False),
        sa.Column("saved_at", sa.DateTime(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["trend_id"], ["trends.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "trend_id", name="uq_user_saved_trend"),
    )
    op.create_index(op.f("ix_saved_trends_id"), "saved_trends", ["id"])
    op.create_index(op.f("ix_saved_trends_saved_at"), "saved_trends", ["saved_at"])
    op.create_index(op.f("ix_saved_trends_trend_id"), "saved_trends", ["trend_id"])
    op.create_index(op.f("ix_saved_trends_user_id"), "saved_trends", ["user_id"])

    op.create_table(
        "trend_embeddings",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("trend_id", sa.String(), nullable=False),
        sa.Column("embedding", sa.JSON(), nullable=False),
        sa.Column("embedding_model", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["trend_id"], ["trends.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_trend_embeddings_id"), "trend_embeddings", ["id"])
    op.create_index(op.f("ix_trend_embeddings_trend_id"), "trend_embeddings", ["trend_id"])

    op.create_table(
        "trend_sources",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("trend_id", sa.String(), nullable=False),
        sa.Column("source_type", sa.String(), nullable=False),
        sa.Column("source_url", sa.String(), nullable=True),
        sa.Column("source_id", sa.String(), nullable=True),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("author", sa.String(), nullable=True),
        sa.Column("upvotes", sa.Integer(), nullable=True),
        sa.Column("downvotes", sa.Integer(), nullable=True),
        sa.Column("comments", sa.Integer(), nullable=True),
        sa.Column("shares", sa.Integer(), nullable=True),
        sa.Column("published_at", sa.DateTime(), nullable=True),
        sa.Column("fetched_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["trend_id"], ["trends.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("trend_id", "source_type", "source_id", name="uq_trend_source"),
    )
    op.create_index("idx_source_type", "trend_sources", ["source_type"])
    op.create_index(op.f("ix_trend_sources_id"), "trend_sources", ["id"])
    op.create_index(op.f("ix_trend_sources_source_id"), "trend_sources", ["source_id"])
    op.create_index(op.f("ix_trend_sources_source_type"), "trend_sources", ["source_type"])
    op.create_index(op.f("ix_trend_sources_trend_id"), "trend_sources", ["trend_id"])


def downgrade() -> None:
    op.drop_table("trend_sources")
    op.drop_table("trend_embeddings")
    op.drop_table("saved_trends")
    op.drop_table("reports")
    op.drop_table("alerts")
    op.drop_table("agent_executions")
    op.drop_table("trends")
    op.drop_table("users")
