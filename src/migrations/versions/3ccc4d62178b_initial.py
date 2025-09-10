"""Initial

Revision ID: 3ccc4d62178b
Revises: 
Create Date: 2025-07-14 20:27:51.503379

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '3ccc4d62178b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url_s3', sa.String(length=10840), nullable=False),
    sa.Column('url_hashed', sa.String(length=10840), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
