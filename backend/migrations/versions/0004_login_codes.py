"""Add login codes table.

Revision ID: 0004_login_codes
Revises: 0003_subscriptions
Create Date: 2026-06-08
"""

from alembic import op
import sqlalchemy as sa

revision = "0004_login_codes"
down_revision = "0003_subscriptions"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "login_codes",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("code_hash", sa.String(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("consumed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_login_codes_created_at"), "login_codes", ["created_at"])
    op.create_index(op.f("ix_login_codes_email"), "login_codes", ["email"])
    op.create_index(op.f("ix_login_codes_expires_at"), "login_codes", ["expires_at"])
    op.create_index(op.f("ix_login_codes_id"), "login_codes", ["id"])


def downgrade() -> None:
    op.drop_index(op.f("ix_login_codes_id"), table_name="login_codes")
    op.drop_index(op.f("ix_login_codes_expires_at"), table_name="login_codes")
    op.drop_index(op.f("ix_login_codes_email"), table_name="login_codes")
    op.drop_index(op.f("ix_login_codes_created_at"), table_name="login_codes")
    op.drop_table("login_codes")
