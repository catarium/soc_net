from typing import List, Optional

from app.db.models.user import User
from app.db.repositories.subscription import SubscriptionRepository
from app.db.repositories.user import UserRepository
from app.db.repositories.media import MediaRepository
from app.utils.password_hashing.hash_password import get_password_hash

from pydantic import BaseModel, Field
from fastapi import HTTPException


class ProfilePictureCreatorResponseSchema(BaseModel):
    id: int
    name: str

    @staticmethod
    def from_sqlalchemy(orm_model):
        return ProfilePictureCreatorResponseSchema(
            id=orm_model.id,
            name=orm_model.name
        )


class ProfilePictureResponseSchema(BaseModel):
    creator: ProfilePictureCreatorResponseSchema
    content_type: str
    filename: str

    @staticmethod
    def from_sqlalchemy(orm_model):
        if not orm_model:
            return None
        return ProfilePictureResponseSchema(
            creator=ProfilePictureCreatorResponseSchema.from_sqlalchemy(
                orm_model.creator),
            content_type=orm_model.content_type,
            filename=orm_model.filename
        )


class UserCreateResponseSchema(BaseModel):
    id: int
    name: str
    password: str
    profile_picture: Optional[ProfilePictureResponseSchema]


class AdminUserGetResponseSchema(BaseModel):
    id: int
    name: str
    password: str
    profile_picture: Optional[ProfilePictureResponseSchema]


class SubscriptionUserGetResponseSchema(BaseModel):
    id: int
    name: str
    profile_picture: Optional[ProfilePictureResponseSchema]


class UserGetResponseSchema(BaseModel):
    id: int
    name: str
    subscriptions: List[SubscriptionUserGetResponseSchema]
    profile_picture: Optional[ProfilePictureResponseSchema]


class PersonalUserGetResponseSchema(BaseModel):
    id: int
    name: str
    subscriptions: List[SubscriptionUserGetResponseSchema]
    profile_picture: Optional[ProfilePictureResponseSchema]


class UserService:
    async def create(self, name: str,
                     password: str, profile_picture: str) -> UserCreateResponseSchema:
        profile_picture_obj = await MediaRepository().get_by_id(profile_picture)
        if not profile_picture_obj:
            raise HTTPException(status_code=404, detail="media not found")
        hashed_password = get_password_hash(password)
        db_obj = await UserRepository().get_by_name(name)
        if db_obj:
            raise HTTPException(status_code=400, detail='name is occupied')
        db_obj = await UserRepository().create(name=name,
                                               password=hashed_password, profile_picture=profile_picture_obj)
        return UserCreateResponseSchema(
            id=db_obj.id,
            name=db_obj.name,
            password=db_obj.password,
            profile_picture=ProfilePictureResponseSchema.from_sqlalchemy(
                db_obj.profile_picture)
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
            profile_picture=ProfilePictureResponseSchema.from_sqlalchemy(
                db_obj.profile_picture),
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
            profile_picture=ProfilePictureResponseSchema.from_sqlalchemy(
                db_obj.profile_picture),
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
            profile_picture=ProfilePictureResponseSchema.from_sqlalchemy(
                db_obj.profile_picture),
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
            profile_picture=ProfilePictureResponseSchema.from_sqlalchemy(
                db_obj.profile_picture),
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
            profile_picture=ProfilePictureResponseSchema.from_sqlalchemy(
                db_obj.profile_picture),
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
                                                      profile_picture=ProfilePictureResponseSchema.from_sqlalchemy
                                        (
                                                          s.profile_picture),
                                                      name=s.subscriber.name)
                    for s in subscriptions]
        elif type == 'subscriber_id':
            return [SubscriptionUserGetResponseSchema(id=s.user.id,
                                                      profile_picture=ProfilePictureResponseSchema.from_sqlalchemy
                                        (
                                                          s.profile_picture),
                                                      name=s.user.name)
                    for s in subscriptions]
