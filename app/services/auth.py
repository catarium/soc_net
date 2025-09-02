from fastapi import HTTPException, Request
from pydantic import BaseModel

from app.db.repositories.user import UserRepository
from app.db.repositories.media import MediaRepository
from app.utils.password_hashing.hash_password import get_password_hash
from app.utils.password_hashing.verify_password import verify_password


class UserRegisterResponseSchema(BaseModel):
    id: int
    name: str


class UserLoginResponseSchema(BaseModel):
    id: int
    name: str


class AuthService:
    async def check_password(self, request: Request, name, password):
        '''
        compares password with password of said user
        :param request: fastapi request object with session
        :param name: name of user
        :param password: password to check
        :return: success
        :raises HTTPException: if user is not found or password is incorrect
        '''
        user = await UserRepository().get_by_name(name=name)
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=400, detail='login failed')
        request.session['user_id'] = user.id
        return UserLoginResponseSchema(
            id=user.id,
            name=user.name,
        )

    async def register_user(self, request, name, password, profile_picture):
        hashed_password = get_password_hash(password)
        db_obj = await UserRepository().get_by_name(name)
        if db_obj:
            raise HTTPException(status_code=400, detail='name is occupied')
        profile_picture_obj = await MediaRepository().get_by_id(profile_picture)
        if not profile_picture_obj:
            raise HTTPException(status_code=404, detail="media not found")
        db_obj = await UserRepository().create(
            name=name,
            password=hashed_password,
            profile_picture=profile_picture_obj,
        )
        request.session['user_id'] = db_obj.id
        return UserRegisterResponseSchema(
            id=db_obj.id,
            name=db_obj.name,
            profile_picture=db_obj.profile_picture
        )
