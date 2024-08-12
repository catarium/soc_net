from typing import Optional

from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel, Field

from app.deps.auth.user_level import session_user
from app.services.post import PostService
from app.services.user import UserService
from app.utils.response import Response

router = APIRouter(prefix='')


class PostUpdateRequestSchema(BaseModel):
    post_id: int
    name: Optional[str] = Field(max_length=120, default=None)
    text: Optional[str] = Field(default=None)
    media: list[str] = None


@router.put('/',)
async def update(request: Request, post_schema: PostUpdateRequestSchema, user=Depends(session_user)):
    res = await PostService().update(
        creator_id=user.id,
        **post_schema.model_dump(exclude_unset=True)
    )
    return Response(res=res)
