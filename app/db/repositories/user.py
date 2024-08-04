from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.db.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_name(self, name) -> User | None:
        res = await self.select(name=name)
        if not res:
            return None
        return res[0]

    async def add_subscription(self, subscriber_id, user_id):
        subscriber = await self.get_by_id(subscriber_id)
        user = await self.get_by_id(user_id)
        subscriber.subscriptions.append(user)
        session: AsyncSession
        async with self._get_session() as session:
            session.add(subscriber)
            await session.commit()
            await session.refresh(subscriber)
            return subscriber

    async def delete_subscription(self, subscriber_id, user_id):
        subscriber = await self.get_by_id(subscriber_id)
        user = await self.get_by_id(user_id)
        del subscriber.subscriptions[
            list(map(lambda x: x.id, subscriber.subscriptions)).index(user_id)]
        session: AsyncSession
        async with self._get_session() as session:
            session.add(subscriber)
            await session.commit()
            await session.refresh(subscriber)
            return subscriber
