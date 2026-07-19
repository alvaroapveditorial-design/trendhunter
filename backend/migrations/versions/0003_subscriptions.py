"""Add subscriptions table.

Revision ID: 0003_subscriptions
Revises: 0002_beta_signups
Create Date: 2026-06-08
"""

from alembic import op
import sqlalchemy as sa

revision = "0003_subscriptions"
down_revision = "0002_beta_signups"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "subscriptions",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("plan", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("stripe_customer_id", sa.String(), nullable=True),
        sa.Column("stripe_subscription_id", sa.String(), nullable=True),
        sa.Column("stripe_checkout_session_id", sa.String(), nullable=True),
        sa.Column("current_period_end", sa.DateTime(), nullable=True),
        sa.Column("trial_end", sa.DateTime(), nullable=True),
        sa.Column("cancel_at_period_end", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_subscriptions_created_at"), "subscriptions", ["created_at"])
    op.create_index(op.f("ix_subscriptions_email"), "subscriptions", ["email"])
    op.create_index(op.f("ix_subscriptions_id"), "subscriptions", ["id"])
    op.create_index(op.f("ix_subscriptions_plan"), "subscriptions", ["plan"])
    op.create_index(op.f("ix_subscriptions_status"), "subscriptions", ["status"])
    op.create_index(
        op.f("ix_subscriptions_stripe_checkout_session_id"),
        "subscriptions",
        ["stripe_checkout_session_id"],
        unique=True,
    )
    op.create_index(
        op.f("ix_subscriptions_stripe_customer_id"),
        "subscriptions",
        ["stripe_customer_id"],
    )
    op.create_index(
        op.f("ix_subscriptions_stripe_subscription_id"),
        "subscriptions",
        ["stripe_subscription_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_subscriptions_stripe_subscription_id"), table_name="subscriptions")
    op.drop_index(op.f("ix_subscriptions_stripe_customer_id"), table_name="subscriptions")
    op.drop_index(op.f("ix_subscriptions_stripe_checkout_session_id"), table_name="subscriptions")
    op.drop_index(op.f("ix_subscriptions_status"), table_name="subscriptions")
    op.drop_index(op.f("ix_subscriptions_plan"), table_name="subscriptions")
    op.drop_index(op.f("ix_subscriptions_id"), table_name="subscriptions")
    op.drop_index(op.f("ix_subscriptions_email"), table_name="subscriptions")
    op.drop_index(op.f("ix_subscriptions_created_at"), table_name="subscriptions")
    op.drop_table("subscriptions")
