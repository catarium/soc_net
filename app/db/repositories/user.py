from app.db.models.user import User
from app.db.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_name(self, name) -> User | None:
        res = await self.select(name=name)
        if not res:
            return None
        return res[0]

    async def subscribe_user(self, user_id, subscriber_id):
        user = await self.get_by_id(user_id)
        subscriber = await UserRepository().get_by_id(subscriber_id)
        print(user.subscriptions)
        return user
