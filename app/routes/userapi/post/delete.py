from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel, Field

from app.deps.auth.user_level import session_user
from app.services.post import PostService
from app.services.user import UserService
from app.utils.response import Response

router = APIRouter(prefix='')


@router.delete('/{post_id}')
async def delete(request: Request, post_id: int, user=Depends(session_user)):
    res = await PostService().delete(
        creator_id=user.id,
        post_id=post_id
    )
    return Response(res=res)
