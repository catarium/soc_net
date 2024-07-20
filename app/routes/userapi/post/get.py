from typing import Optional

from fastapi import APIRouter, Request, Query, Depends
from pydantic import BaseModel, Field

from app.services.post import PostService
from app.services.user import UserService
from app.utils.response import Response

router = APIRouter(prefix='')


class PostGetSchema(BaseModel):
    name: Optional[str] = None
    creator_id: Optional[int] = None
    offset: int = 0
    limit: int = 10


@router.get('/{post_id}')
async def get(request: Request, post_id: int):
    res = await PostService().get_by_id(post_id)
    return Response(post=res)


@router.get('/')
async def search(request: Request, post_schema: PostGetSchema=Depends()):
    res = await PostService().get(
        offset=post_schema.offset,
        limit=post_schema.limit,
        name=post_schema.name,
        creator_id=post_schema.creator_id
    )
    return Response(res=res)
