from typing import List
from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Post(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    creator: Mapped["User"] = relationship(
        lazy='joined',
        uselist=False
    )
    name: Mapped[str] = mapped_column(String(120))
    text: Mapped[str]
