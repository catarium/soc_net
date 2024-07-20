"""subscribers

Revision ID: ae2fd623ba86
Revises: 96923747d723
Create Date: 2024-07-17 19:45:20.142082

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae2fd623ba86'
down_revision: Union[str, None] = '96923747d723'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
