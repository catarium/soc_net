from typing import List
from typing import Optional

from sqlalchemy import String, ForeignKey, TIMESTAMP, func
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

from app.db.models.media import Media, MediaPosts
from app.utils.datetime_utils import aware_utcnow


class Post(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    creator: Mapped["User"] = relationship(
        lazy='joined',
        uselist=False
    )
    updated_time: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=False),
                                                          nullable=True)
    name: Mapped[str] = mapped_column(String(120))
    text: Mapped[Optional[str]] = mapped_column(nullable=True)
    media_assocs: Mapped[list['MediaPosts']] = relationship(
        'MediaPosts',
        lazy='selectin',
        cascade='all, delete-orphan',
    )
    media: Mapped[list['Media']] = association_proxy(
        'media_assocs', 'media',
        creator=lambda media: MediaPosts(media=media)
    )
