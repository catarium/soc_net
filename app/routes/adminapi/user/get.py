from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

from app.services.user import UserService
from app.utils.response import Response

router = APIRouter(prefix='')


@router.get('/{user_id}')
async def get(request: Request, user_id: int):
    res = await UserService().get_by_id_admin(user_id)
    return Response(user=res)
