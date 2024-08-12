from fastapi import APIRouter, Depends

from app.deps.auth.user_level import session_user
from app.services.comment import CommentService
from app.utils.response import Response

router = APIRouter(prefix='')


@router.delete('/{comment_id}')
async def delete(comment_id: int, creator=Depends(session_user)):
    res = await CommentService().delete(
        creator_id=creator.id,
        comment_id=comment_id
    )
    return Response(res=res)
