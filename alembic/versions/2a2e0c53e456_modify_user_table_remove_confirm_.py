from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2a2e0c53e456'
down_revision = 'a847c1bd05e3'
branch_labels = None
depends_on = None

def upgrade():
    # Add the `mobile_number` column
    op.add_column('users', sa.Column('mobile_number', sa.String(length=15), nullable=True))

    # Drop the `confirm_password` column
    op.drop_column('users', 'confirm_password')


def downgrade():
    # Reverse the changes
    op.add_column('users', sa.Column('confirm_password', sa.String(length=255), nullable=True))
    op.drop_column('users', 'mobile_number')
