"""add_admin

Revision ID: 728b159782ae
Revises: 74dcbd6970f3
Create Date: 2024-07-05 22:39:40.640404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '728b159782ae'
down_revision: Union[str, None] = '74dcbd6970f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('admin', sa.Boolean(), server_default='false', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'admin')
    # ### end Alembic commands ###
