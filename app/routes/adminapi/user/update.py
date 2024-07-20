from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel, Field

from app.deps.auth.user_level import session_user
from app.services.post import PostService
from app.services.user import UserService
from app.utils.response import Response

router = APIRouter(prefix='')


class PostCreateSchema(BaseModel):
    post_id: int
    name: str = Field(max_length=120)
    text: str = Field()


@router.post('/',)
async def create(request: Request, post_schema: PostCreateSchema, user=Depends(session_user)):
    res = await PostService().create(
        name=post_schema.name,
        text=post_schema.text,
        creator_id=user.id
    )
    return Response(post=res)