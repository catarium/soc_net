from app.db.models.user import User
from app.db.repositories.user import UserRepository
from app.utils.password_hashing.hash_password import get_password_hash

from pydantic import BaseModel, Field
from fastapi import HTTPException


class UserCreateResponseSchema(BaseModel):
    id: int
    name: str
    password: str


class AdminUserGetResponseSchema(BaseModel):
    id: int
    name: str
    password: str


class UserGetResponseSchema(BaseModel):
    id: int
    name: str


class PersonalUserGetResponseSchema(BaseModel):
    id: int
    name: str


class UserService:
    async def create(self, name: str,
                     password: str) -> UserCreateResponseSchema:
        hashed_password = get_password_hash(password)
        db_obj = await UserRepository().get_by_name(name)
        if db_obj:
            raise HTTPException(status_code=400, detail='name is occupied')
        db_obj = await UserRepository().create(name=name,
                                               password=hashed_password)
        return UserCreateResponseSchema(
                                        id=db_obj.id,
                                        name=db_obj.name,
                                        password=db_obj.password
        )

    async def get_by_id_admin(self, user_id) -> AdminUserGetResponseSchema:
        """
        looks up for user by id
        :param user_id: user id
        :return: user with password hash
        :raises HTTPException: if user is not found
        """
        db_obj = await UserRepository().get_by_id(user_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail='user not found')
        return AdminUserGetResponseSchema(
                                     name=db_obj.name,
                                     password=db_obj.password,
                                     id=db_obj.id
        )

    async def get_personal(self, user_id) -> PersonalUserGetResponseSchema:
        db_obj = await UserRepository().get_by_id(user_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail='user not found')
        return PersonalUserGetResponseSchema(
            name=db_obj.name,
            id=db_obj.id
        )

    async def get_by_id(self, user_id) -> UserGetResponseSchema:
        """
        looks up for user by id
        :param user_id: user id
        :return: user
        :raises HTTPException: if user is not found
        """
        db_obj = await UserRepository().get_by_id(user_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail='user not found')
        return UserGetResponseSchema(
            name=db_obj.name,
            id=db_obj.id
        )

    async def subscribe_user(self, user_id, subscriber_id):
        await UserRepository().subscribe_user(user_id, subscriber_id)
        return True

    # async def get_by_name(self, name):
    #     db_obj = await UserRepository().select(name=name)
    #     if not db_obj:
