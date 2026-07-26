"""Add opportunity_brief column to trends.

Revision ID: 0005_opportunity_brief
Revises: 0004_login_codes
Create Date: 2026-07-26
"""

from alembic import op
import sqlalchemy as sa

revision = "0005_opportunity_brief"
down_revision = "0004_login_codes"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "trends",
        sa.Column("opportunity_brief", sa.JSON(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("trends", "opportunity_brief")
