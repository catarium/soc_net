
"""enable autoincrement properly using setval()

Revision ID: f5533407a7d0
Revises: 0cbc8e146b49
Create Date: 2025-07-02 10:23:53
"""
from alembic import op
import sqlalchemy as sa

revision = 'f5533407a7d0'
down_revision = '0cbc8e146b49'
branch_labels = None
depends_on = None

def upgrade():
    for table in ('media_posts', 'media_comments'):
        seq = f"{table}_id_seq"
        op.execute(f"CREATE SEQUENCE IF NOT EXISTS {seq}")
        op.execute(
            f"SELECT setval('{seq}', COALESCE((SELECT MAX(id) FROM {table}), 1))"
        )
        op.alter_column(
            table, 'id',
            existing_type=sa.Integer(),
            server_default=sa.text(f"nextval('{seq}')")
        )

def downgrade():
    for table in ('media_posts', 'media_comments'):
        seq = f"{table}_id_seq"
        op.alter_column(
            table, 'id',
            existing_type=sa.Integer(),
            server_default=None
        )
        op.execute(f"DROP SEQUENCE IF EXISTS {seq}")

