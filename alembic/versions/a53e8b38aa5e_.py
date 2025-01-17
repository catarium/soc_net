"""empty message

Revision ID: a53e8b38aa5e
Revises: 
Create Date: 2024-08-08 19:57:38.513774

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a53e8b38aa5e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('admin', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('password', sa.String(length=1024), nullable=False),
    sa.Column('creation_time', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('media',
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.Column('content_type', sa.String(), nullable=False),
    sa.Column('filename', sa.String(), nullable=False),
    sa.Column('creation_time', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('filename'),
    sa.UniqueConstraint('filename')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.Column('updated_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('creation_time', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subscriptions',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('subscriber_id', sa.Integer(), nullable=False),
    sa.Column('creation_time', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['subscriber_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'subscriber_id')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('creation_time', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('media_posts',
    sa.Column('media_id', sa.String(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('creation_time', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['media_id'], ['media.filename'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('media_id', 'post_id')
    )
    op.create_table('media_comments',
    sa.Column('media_id', sa.String(), nullable=False),
    sa.Column('comment_id', sa.Integer(), nullable=False),
    sa.Column('creation_time', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], ),
    sa.ForeignKeyConstraint(['media_id'], ['media.filename'], ),
    sa.PrimaryKeyConstraint('media_id', 'comment_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('media_comments')
    op.drop_table('media_posts')
    op.drop_table('comments')
    op.drop_table('subscriptions')
    op.drop_table('posts')
    op.drop_table('media')
    op.drop_table('users')
    # ### end Alembic commands ###
