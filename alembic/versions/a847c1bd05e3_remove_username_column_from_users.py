from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a847c1bd05e3'
down_revision = 'cdbdd87471d9'
branch_labels = None
depends_on = None


def upgrade():
    # Drop the `username` column from the `users` table
    op.drop_column('users', 'username')


def downgrade():
    # Re-add the `username` column to the `users` table
    op.add_column(
        'users',
        sa.Column('username', sa.String(length=50), nullable=True)
    )
