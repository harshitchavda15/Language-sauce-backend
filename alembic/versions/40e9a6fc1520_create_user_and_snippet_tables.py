"""Create User and Snippet tables

Revision ID: 40e9a6fc1520
Revises: ddc3c1434051
Create Date: 2024-12-30 19:33:30.817651

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '40e9a6fc1520'
down_revision: Union[str, None] = 'ddc3c1434051'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_otps_email', table_name='otps')
    op.drop_index('ix_otps_id', table_name='otps')
    op.drop_table('otps')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('otps',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('otp', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('expires_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.Column('is_used', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('attempts', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='otps_pkey')
    )
    op.create_index('ix_otps_id', 'otps', ['id'], unique=False)
    op.create_index('ix_otps_email', 'otps', ['email'], unique=False)
    # ### end Alembic commands ###
