from datetime import datetime
from typing import Any

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    creation_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False),
                                                    server_default=func.now())
