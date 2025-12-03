"""creating users table

Revision ID: 20b4f2d21b1e
Revises: 
Create Date: 2025-12-01 11:17:15.458336

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20b4f2d21b1e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("first_name", sa.String, nullable=False),
        sa.Column("last_name", sa.String, nullable=True),
        sa.Column("email", sa.String, nullable=False, unique=True),
        sa.Column("profile_pic", sa.String, nullable=True),
        sa.Column("country", sa.String, nullable=True),
        sa.Column("fav_team", sa.String, nullable=True),
        sa.Column("created_at", sa.TIMESTAMP, nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("user")
