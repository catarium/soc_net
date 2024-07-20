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
async def create(request: Request, subscriber_schema: SubscriptionCreateSchema, user=Depends(session_user)):
    res = await UserService().subscribe_user(subscriber_schema.user_id, user.id)
    return Response()
