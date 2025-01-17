from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ee1792055b81'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Drop the foreign key constraint
    op.drop_constraint("snippets_ibfk_1", "snippets", type_="foreignkey")
    
    # Drop the 'snippets' table
    op.drop_table("snippets")
    
    # Drop the 'users' table
    op.drop_table("users")

def downgrade() -> None:
    # Recreate 'users' table
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("username", sa.String(255), unique=True, nullable=False),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
    )

    # Recreate 'snippets' table
    op.create_table(
        "snippets",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("code", sa.Text, nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
    )
