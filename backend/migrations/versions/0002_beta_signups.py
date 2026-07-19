"""Add beta signups table.

Revision ID: 0002_beta_signups
Revises: 0001_initial_schema
Create Date: 2026-06-07
"""

from alembic import op
import sqlalchemy as sa

revision = "0002_beta_signups"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "beta_signups",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("interests", sa.JSON(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_beta_signups_created_at"), "beta_signups", ["created_at"])
    op.create_index(op.f("ix_beta_signups_email"), "beta_signups", ["email"], unique=True)
    op.create_index(op.f("ix_beta_signups_id"), "beta_signups", ["id"])
    op.create_index(op.f("ix_beta_signups_status"), "beta_signups", ["status"])


def downgrade() -> None:
    op.drop_index(op.f("ix_beta_signups_status"), table_name="beta_signups")
    op.drop_index(op.f("ix_beta_signups_id"), table_name="beta_signups")
    op.drop_index(op.f("ix_beta_signups_email"), table_name="beta_signups")
    op.drop_index(op.f("ix_beta_signups_created_at"), table_name="beta_signups")
    op.drop_table("beta_signups")
