from typing import Optional, Literal

from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel, Field

from app.deps.auth.user_level import session_user
from app.services.post import PostService
from app.services.user import UserService
from app.utils.response import Response

router = APIRouter(prefix='')


class SubscriptionGetRequestSchema(BaseModel):
    type: Literal['user_id', 'subscriber_id']
    user_id: int = None
    offset: int = 0
    limit: int = 10


@router.get('/', )
async def get(
        request: Request,
        subscription_schema: SubscriptionGetRequestSchema = Depends(),
        user=Depends(session_user)
):
    res = await UserService().get_by_subscription(subscription_schema.type,
                                            subscription_schema.user_id,
                                            subscription_schema.offset,
                                            subscription_schema.limit
                                            )
    return Response(res=res)
