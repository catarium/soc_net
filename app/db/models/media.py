from typing import List
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class MediaPosts(Base):
    __tablename__ = 'media_posts'
    media_id: Mapped[int] = mapped_column(ForeignKey('media.filename'),
                                          primary_key=True
                                          )

    media: Mapped["Media"] = relationship(
        lazy='joined',
        uselist=False,
        foreign_keys=[media_id]
    )
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'),
                                         primary_key=True)
    post: Mapped["Post"] = relationship(
        lazy='joined',
        uselist=False,
        foreign_keys=[post_id]
    )


class MediaComments(Base):
    __tablename__ = 'media_comments'
    media_id: Mapped[int] = mapped_column(ForeignKey('media.filename'),
                                          primary_key=True
                                          )
    media: Mapped["Media"] = relationship(
        lazy='joined',
        uselist=False,
        foreign_keys=[media_id]
    )
    comment_id: Mapped[int] = mapped_column(ForeignKey('comments.id'),
                                         primary_key=True)
    comment: Mapped["Comment"] = relationship(
        lazy='joined',
        uselist=False,
        foreign_keys=[comment_id]
    )


class Media(Base):
    __tablename__ = 'media'
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    creator: Mapped["User"] = relationship(
        lazy='joined',
        uselist=False
    )
    content_type: Mapped[str] = mapped_column()
    filename: Mapped[str] = mapped_column(primary_key=True, unique=True)