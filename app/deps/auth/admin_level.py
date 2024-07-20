from fastapi import HTTPException, Request

from app.db.repositories.user import UserRepository


async def session_admin(request: Request):
    if 'user_id' not in request.session:
        raise HTTPException(status_code=401, detail='not logged in')
    user = await UserRepository().get_by_id(obj_id=request.session['user_id'])
    if not user:
        raise HTTPException(status_code=401, detail='not logged in')
    if not user.admin:
        raise HTTPException(status_code=401, detail='not admin')
    return user
