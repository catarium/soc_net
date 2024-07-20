from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel, Field

from app.deps.auth.user_level import session_user
from app.services.post import PostService
from app.services.user import UserService
from app.utils.response import Response

router = APIRouter(prefix='')


class PostUpdateSchema(BaseModel):
    id: int
    name: str = Field(max_length=120, default='')
    text: str = Field()


@router.put('/',)
async def update(request: Request, post_schema: PostUpdateSchema, user=Depends(session_user)):
    res = await PostService().update(
        post_id=post_schema.id,
        name=post_schema.name,
        text=post_schema.text,
        creator_id=user.id
    )
    return Response(res=res)