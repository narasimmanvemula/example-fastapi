"""add  user table

Revision ID: f0c2a36cb53d
Revises: a4d6a3f03dc4
Create Date: 2026-06-13 13:42:27.338177

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0c2a36cb53d'
down_revision: Union[str, Sequence[str], None] = 'a4d6a3f03dc4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
