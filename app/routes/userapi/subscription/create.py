from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel, Field

from app.deps.auth.user_level import session_user
from app.services.post import PostService
from app.services.user import UserService
from app.utils.response import Response


router = APIRouter(prefix='')


class SubscriptionCreateSchema(BaseModel):
    user_id: int


@router.post('/',)
async def create(
        request: Request,
        subscription_schema: SubscriptionCreateSchema,
        user=Depends(session_user)
):
    res = await UserService().add_subscription(
        user.id,
        subscription_schema.user_id,
    )
    return Response(res=res)
