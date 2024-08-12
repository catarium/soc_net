from typing import Optional

from fastapi import APIRouter, Request, Query, Depends
from pydantic import BaseModel, Field

from app.services.post import PostService
from app.services.user import UserService
from app.utils.datetime_utils import aware_utcnow
from app.utils.response import Response

router = APIRouter(prefix='')


class PostGetRequestSchema(BaseModel):
    name: Optional[str] = None
    creator_id: Optional[int] = None
    created_before: Optional[float] = aware_utcnow().timestamp()
    created_after: Optional[float] = 0
    offset: int = 0
    limit: int = Field(default=10, ge=1, le=30)


@router.get('/{post_id}')
async def get(request: Request, post_id: int):
    res = await PostService().get_by_id(post_id)
    return Response(post=res)


@router.get('/')
async def search(request: Request,
                 post_schema: PostGetRequestSchema = Depends()):
    res = await PostService().get(
        offset=post_schema.offset,
        limit=post_schema.limit,
        name=post_schema.name,
        creator_id=post_schema.creator_id,
        created_after=post_schema.created_after,
        created_before=post_schema.created_before
    )
    return Response(res=res)
