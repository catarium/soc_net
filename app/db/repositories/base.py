from decimal import Decimal
from types import NoneType
from typing import Any, Generic, TypeVar, Callable, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.db.base_class import Base
from app.db.session import SessionLocal

ModelType = TypeVar('ModelType', bound=Base)


class BaseRepository(Generic[ModelType]):
    model: Callable[..., ModelType]

    async def create(self, **obj_in_data) -> ModelType:
        async with self._get_session() as session:
            db_obj = self.model(**obj_in_data)

            session.add(db_obj)

            await session.commit()
            await session.refresh(db_obj)

            return db_obj

    async def update(self, db_obj: ModelType, **obj_in_data) -> ModelType:
        async with self._get_session() as session:
            for field, value in obj_in_data.items():
                setattr(db_obj, field, value)

            merged_db_obj = await session.merge(db_obj)

            session.add(merged_db_obj)

            await session.commit()
            return db_obj

    async def get_by_id(self, obj_id: int) -> ModelType | None:
        res = (await self.select(id=obj_id))
        if not res:
            return None
        return res[0]

    async def select(
            self,
            custom_where=None,
            custom_order=None,
            custom_limit=None,
            custom_offset=None,
            **filters,
    ) -> List[ModelType]:
        custom_select = select(self.model)
        if custom_where is not None:
            custom_select = custom_select.where(custom_where)
        if custom_order is None:
            custom_select = custom_select.order_by(self.model.id.desc())
        else:
            custom_select = custom_select.order_by(*custom_order)
        if custom_limit:
            custom_select = custom_select.limit(custom_limit)
        if custom_offset:
            custom_select = custom_select.offset(custom_offset)

        session: AsyncSession
        async with self._get_session() as session:
            print(custom_select.filter_by(**filters))
            result = await session.execute(custom_select.filter_by(**filters))
            res = result.scalars().all()
        return res

    async def delete(self, model: ModelType) -> Optional[ModelType]:
        async with self._get_session() as session:
            await session.delete(model)
            await session.commit()
            return model

    @staticmethod
    def _get_session():
        return SessionLocal()
