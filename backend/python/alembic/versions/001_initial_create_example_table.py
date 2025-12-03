"""Initial create example table

Revision ID: 001_initial
Revises: 
Create Date: 2025-12-03 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create example table
    op.create_table(
        'example',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('entry_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('description', sa.String(length=1000), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create index on entry_date
    op.create_index('ix_example_entry_date', 'example', ['entry_date'], unique=False)


def downgrade() -> None:
    # Drop index
    op.drop_index('ix_example_entry_date', table_name='example')
    
    # Drop table
    op.drop_table('example')

