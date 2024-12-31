"""create tables

Revision ID: b8ce15df7294
Revises: b10ee05af318
Create Date: 2024-12-23 09:20:20.168086

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8ce15df7294'
down_revision: Union[str, None] = 'b10ee05af318'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
