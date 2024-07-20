from fastapi import APIRouter, Request, Depends

from app.deps.auth.user_level import session_user
from app.services.user import UserService
from app.utils.response import Response

router = APIRouter(prefix='/me')


@router.get('')
async def me(request: Request, user=Depends(session_user)):
    res = await UserService().get_personal(user.id)
    return Response(res=res)
