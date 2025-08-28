"""add autonumber id to media_posts & media_comments

Revision ID: 0cbc8e146b49
Revises: 93fc04266e23
Create Date: 2025-07-02 09:41:09.329449
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0cbc8e146b49'
down_revision = '93fc04266e23'
branch_labels = None
depends_on = None


def upgrade():
    for table in ['media_posts', 'media_comments']:
        seq = f"{table}_id_seq"

        op.add_column(table, sa.Column('id', sa.Integer(), nullable=True))
        op.execute(f"CREATE SEQUENCE {seq} OWNED BY {table}.id")
        op.alter_column(table, 'id', server_default=sa.text(f"nextval('{seq}')"))
        op.execute(f"UPDATE {table} SET id = nextval('{seq}') WHERE id IS NULL")
        op.drop_constraint(f"{table}_pkey", table, type_='primary')
        op.alter_column(table, 'id', nullable=False, server_default=None)
        op.create_primary_key(f"{table}_pkey", table, ['id'])


def downgrade():
    # Reverse order: drop new PKs, drop id columns & sequences, recreate old PKs
    op.drop_constraint('media_comments_pkey', 'media_comments', type_='primary')
    op.drop_column('media_comments', 'id')
    op.execute("DROP SEQUENCE IF EXISTS media_comments_id_seq")

    op.drop_constraint('media_posts_pkey', 'media_posts', type_='primary')
    op.drop_column('media_posts', 'id')
    op.execute("DROP SEQUENCE IF EXISTS media_posts_id_seq")

    # Recreate old composite PKs
    op.create_primary_key('media_comments_pkey', 'media_comments', ['media_id', 'comment_id'])
    op.create_primary_key('media_posts_pkey', 'media_posts', ['media_id', 'post_id'])

