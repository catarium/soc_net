from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel, Field

from app.deps.auth.user_level import session_user
from app.services.comment import CommentService
from app.services.post import PostService
from app.services.user import UserService
from app.utils.response import Response

router = APIRouter(prefix='')


class CommentCreateRequestSchema(BaseModel):
    post_id: int
    text: str


@router.post('/',)
async def create(request: Request,
                 comment_schema: CommentCreateRequestSchema,
                 user=Depends(session_user)
                 ):
    res = await CommentService().create(creator_id=user.id,
                                  post_id=comment_schema.post_id,
                                  text=comment_schema.text
                                  )
    return Response(res=res)