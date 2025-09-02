from typing import List
from typing import Optional

from sqlalchemy import String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from app.db.base_class import Base


# subscriptions = Table(
#     "subscriptions",
#     Base.metadata,
#     Column("user_id", ForeignKey("myuser.id")),
#     Column("subscriber_id", ForeignKey("myuser.id")),
# )


class Subscription(Base):
    __tablename__ = 'subscriptions'
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id",),
                                         primary_key=True,
                                         )
    user: Mapped["User"] = relationship(
        lazy='joined',
        uselist=False,
        foreign_keys=[user_id],
        viewonly=True,
    )
    subscriber_id: Mapped[int] = mapped_column(ForeignKey("users.id"),
                                               primary_key=True
                                               )
    subscriber: Mapped["User"] = relationship(
        lazy='joined',
        uselist=False,
        foreign_keys=[subscriber_id],
        viewonly=True,
    )


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    admin: Mapped[bool] = mapped_column(server_default='false')
    password: Mapped[str] = mapped_column(String(1024))
    profile_picture_id: Mapped[int] = mapped_column(ForeignKey('media.filename'),
                                                    nullable=True,
                                                    )
    profile_picture: Mapped["Media"] = relationship(
        foreign_keys=[profile_picture_id],
        lazy='selectin'
    )
    subscriptions: Mapped[List["User"]] = relationship(
        lazy='selectin',
        secondary='subscriptions',
        primaryjoin=(Subscription.subscriber_id == id),
        secondaryjoin=(Subscription.user_id == id),
        join_depth=2,
    )
