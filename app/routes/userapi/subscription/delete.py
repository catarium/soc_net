from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel, Field

from app.deps.auth.user_level import session_user
from app.services.post import PostService
from app.services.user import UserService
from app.utils.response import Response


router = APIRouter(prefix='')


@router.delete('/{user_id}',)
async def delete(
        request: Request,
        user_id: int,
        user=Depends(session_user)
):
    res = await UserService().delete_subscription(user.id, user_id)
    return Response(res=res)
