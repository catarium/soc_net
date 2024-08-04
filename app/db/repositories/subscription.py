from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import Subscription
from app.db.repositories.base import BaseRepository


class SubscriptionRepository(BaseRepository[Subscription]):
    model = Subscription

    async def get_by_user_id(self, offset, limit, **filters):
        res = (await self.select(custom_offset=offset,
                                 custom_limit=limit,
                                 custom_order=(self.model.user_id.desc(),
                                               self.model.subscriber_id.desc()
                                               ),
                                 **filters)
               )
        if not res:
            return None
        return res
