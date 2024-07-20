import time
from typing import Annotated

from fastapi import APIRouter, Request, Depends

from app.db.models.user import User
from app.deps.auth.user_level import session_user

router_get = APIRouter(prefix='/get')


@router_get.get('')
async def test(request: Request):
    res = request.session.get('user_id', 'no data')
    return {'result': res}
