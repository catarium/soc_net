from datetime import datetime
from typing import List
from typing import Optional

from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Comment(Base):
    __tablename__ = 'comments'
    id: Mapped[int] = mapped_column(primary_key=True)
    updated_time: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=False),
        nullable=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    creator: Mapped["User"] = relationship(
        lazy='joined',
        uselist=False
    )
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    post: Mapped["Post"] = relationship(
        lazy='joined',
        uselist=False
    )
    text: Mapped[str]
    media: Mapped[List["Media"]] = relationship(
        lazy='selectin',
        secondary='media_comments',
        uselist=True
    )
