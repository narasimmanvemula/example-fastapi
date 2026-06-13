"""add content column to posts table

Revision ID: a4d6a3f03dc4
Revises: eb2289ec9c89
Create Date: 2026-06-13 13:02:51.727062 
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4d6a3f03dc4'
down_revision: Union[str, Sequence[str], None] = 'eb2289ec9c89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
