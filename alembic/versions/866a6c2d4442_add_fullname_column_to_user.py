"""Add fullname column to User

Revision ID: 866a6c2d4442
Revises: ee1792055b81
Create Date: 2025-01-06 23:15:33.720752

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '866a6c2d4442'
down_revision: Union[str, None] = 'ee1792055b81'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Apply changes: Add the 'fullname' column to the 'users' table."""
    op.add_column('users', sa.Column('fullname', sa.String(length=100), nullable=False))


def downgrade() -> None:
    """Revert changes: Remove the 'fullname' column from the 'users' table."""
    op.drop_column('users', 'fullname')
