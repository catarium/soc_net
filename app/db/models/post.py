from typing import List
from typing import Optional

from sqlalchemy import String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

from app.utils.datetime_utils import aware_utcnow


class Post(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    creator: Mapped["User"] = relationship(
        lazy='joined',
        uselist=False
    )
    creation_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False),
                                                    server_default=func.now())
    updated_time: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=False),
                                                          nullable=True)
    name: Mapped[str] = mapped_column(String(120))
    text: Mapped[str]
