from typing import List
from typing import Optional

from sqlalchemy import String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from app.db.base_class import Base


subscriptions = Table(
    "subscriptions",
    Base.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("subscriber_id", ForeignKey("user.id")),
)


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    admin: Mapped[bool] = mapped_column(server_default='false')
    password: Mapped[str] = mapped_column(String(1024))
    subscriptions: Mapped[List["User"]] = relationship(
        lazy='selectin',
        secondary=subscriptions,
        primaryjoin=(subscriptions.c.subscriber_id == id),
        secondaryjoin=(subscriptions.c.user_id == id)
    )
