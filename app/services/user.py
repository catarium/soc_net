from typing import List

from app.db.models.user import User
from app.db.repositories.subscription import SubscriptionRepository
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


class SubscriptionUserGetResponseSchema(BaseModel):
    id: int
    name: str


class UserGetResponseSchema(BaseModel):
    id: int
    name: str
    subscriptions: List[SubscriptionUserGetResponseSchema]


class PersonalUserGetResponseSchema(BaseModel):
    id: int
    name: str
    subscriptions: List[SubscriptionUserGetResponseSchema]


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
            id=db_obj.id,
            name=db_obj.name,
            password=db_obj.password,
            subscriptions=[SubscriptionUserGetResponseSchema(id=sbp.id,
                                                             name=sbp.name
                                                             )
                           for sbp in db_obj.subscriptions
                           ]
        )

    async def get_personal(self, user_id) -> PersonalUserGetResponseSchema:
        db_obj = await UserRepository().get_by_id(user_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail='user not found')
        return PersonalUserGetResponseSchema(
            id=db_obj.id,
            name=db_obj.name,
            subscriptions=[SubscriptionUserGetResponseSchema(id=sbp.id,
                                                             name=sbp.name
                                                             )
                           for sbp in db_obj.subscriptions
                           ]
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
            id=db_obj.id,
            name=db_obj.name,
            subscriptions=[SubscriptionUserGetResponseSchema(id=sbp.id,
                                                             name=sbp.name
                                                             )
                           for sbp in db_obj.subscriptions
                           ]
        )

    async def add_subscription(self, subscriber_id, user_id):
        if subscriber_id == user_id:
            raise HTTPException(
                status_code=422,
                detail='subscription to oneself'
            )
        user = await UserRepository().get_by_id(subscriber_id)
        if user_id in list(map(lambda x: x.id, user.subscriptions)):
            raise HTTPException(
                status_code=400,
                detail='subscription already exists'
            )
        db_obj = await UserRepository().add_subscription(subscriber_id,
                                                         user_id)
        return PersonalUserGetResponseSchema(
            id=db_obj.id,
            name=db_obj.name,
            subscriptions=[SubscriptionUserGetResponseSchema(id=sbp.id,
                                                             name=sbp.name
                                                             )
                           for sbp in db_obj.subscriptions
                           ]
        )

    async def delete_subscription(self, subscriber_id, user_id):
        subscriber = await UserRepository().get_by_id(subscriber_id)
        if user_id not in list(map(lambda x: x.id, subscriber.subscriptions)):
            raise HTTPException(status_code=404,
                                detail='user does not exist or is not '
                                       'subscribed '
                                )
        db_obj = await UserRepository().delete_subscription(
            subscriber_id,
            user_id
        )
        return PersonalUserGetResponseSchema(
            id=db_obj.id,
            name=db_obj.name,
            subscriptions=[SubscriptionUserGetResponseSchema(id=sbp.id,
                                                             name=sbp.name
                                                             )
                           for sbp in db_obj.subscriptions
                           ]
        )

    async def get_by_subscription(self, type, user_id, offset, limit):
        subscriptions = await SubscriptionRepository().get_by_user_id(
            offset,
            limit,
            **{type: user_id}
        )
        if type == 'user_id':
            return [SubscriptionUserGetResponseSchema(id=s.subscriber.id,
                                                      name=s.subscriber.name)
                    for s in subscriptions]
        elif type == 'subscriber_id':
            return [SubscriptionUserGetResponseSchema(id=s.user.id,
                                                      name=s.user.name)
                    for s in subscriptions]
