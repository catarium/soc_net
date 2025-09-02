from copy import deepcopy
from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import and_

from app.db.models import Post
from app.db.repositories.media import MediaRepository
from app.db.repositories.post import PostRepository
from app.utils.datetime_utils import aware_utcnow, naive_utcnow


class PostMediaUserResponseSchema(BaseModel):
    id: int
    name: str

    @staticmethod
    def from_sqlalchemy(orm_model):
        return PostMediaUserResponseSchema(
            id=orm_model.id,
            name=orm_model.name,
        )


class PostMediaResponseSchema(BaseModel):
    creator: PostMediaUserResponseSchema
    content_type: str
    filename: str

    @staticmethod
    def from_sqlalchemy(orm_model):
        if not orm_model:
            return None
        return PostMediaResponseSchema(
            creator=PostMediaUserResponseSchema.from_sqlalchemy(
                orm_model.creator),
            content_type=orm_model.content_type,
            filename=orm_model.filename
        )


class PostUserResponseSchema(BaseModel):
    id: int
    name: str
    profile_picture: (PostMediaResponseSchema | None)

    @staticmethod
    def from_sqlalchemy(orm_model):
        print("MyLog", PostMediaResponseSchema.from_sqlalchemy(orm_model.profile_picture))
        return PostUserResponseSchema(
            id=orm_model.id,
            name=orm_model.name,
            profile_picture=PostMediaResponseSchema.from_sqlalchemy(orm_model.profile_picture)
        )


class PostCreateResponseSchema(BaseModel):
    id: int
    creation_time: float
    updated: float | None
    name: str
    text: str | None
    media: list[PostMediaResponseSchema]
    creator: PostUserResponseSchema


class PostGetResponseSchema(BaseModel):
    id: int
    creation_time: float
    updated: float | None
    name: str
    text: str | None
    media: list[PostMediaResponseSchema]
    creator: PostUserResponseSchema


class PostUpdateResponseSchema(BaseModel):
    id: int
    creation_time: float
    updated: float | None
    name: str
    text: str | None
    media: list[PostMediaResponseSchema]
    creator: PostUserResponseSchema


class PostDeleteResponseSchema(BaseModel):
    id: int
    creation_time: float
    updated: float | None
    name: str
    text: str | None
    media: list[PostMediaResponseSchema]
    creator: PostUserResponseSchema


class PostService:
    async def create(self, creator_id, name, text, media):
        media_objs = []
        for m in media:
            m_obj = await MediaRepository().get_by_id(m)
            if not m_obj:
                raise HTTPException(status_code=404, detail='media not found')
            media_objs.append(m_obj)
        db_obj = await PostRepository().create(
            creator_id=creator_id,
            name=name,
            text=text,
            media=media_objs
        )
        return PostCreateResponseSchema(
            id=db_obj.id,
            creation_time=db_obj.creation_time.timestamp(),
            updated=(
                db_obj.updated_time.timestamp() if db_obj.updated_time else None),
            name=db_obj.name,
            text=db_obj.text,
            media=[
                PostMediaResponseSchema.from_sqlalchemy(m)
                for m in db_obj.media
            ],
            creator=PostUserResponseSchema.from_sqlalchemy(db_obj.creator),
        )

    async def update(self, creator_id, post_id, **values):
        db_obj = await PostRepository().get_by_id(post_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail='post not found')
        if creator_id != db_obj.creator_id:
            raise HTTPException(
                status_code=403,
                detail='user is not the post creator'
            )
        if 'media' in values:
            media_objs = []
            for m in values['media']:
                m_obj = await MediaRepository().get_by_id(m)
                if not m_obj:
                    raise HTTPException(
                        status_code=404,
                        detail=f'media not found: {m}'
                    )
                media_objs.append(m_obj)
            values['media'] = media_objs
            await PostRepository().update(
                db_obj,
                media=[]
            )
        await PostRepository().update(
            db_obj,
            updated_time=naive_utcnow(),
            **values
        )

        return PostUpdateResponseSchema(
            id=db_obj.id,
            creation_time=db_obj.creation_time.timestamp(),
            updated=db_obj.updated_time.timestamp(),
            name=db_obj.name,
            text=db_obj.text,
            media=[
                PostMediaResponseSchema.from_sqlalchemy(m)
                for m in db_obj.media
            ],
            creator=PostUserResponseSchema.from_sqlalchemy(db_obj.creator)
        )

    async def get_by_id(self, post_id) -> PostGetResponseSchema:
        """
        looks up for post by id
        :param post_id: user id
        :return: post
        :raises HTTPException: if post is not found
        """
        db_obj = await PostRepository().get_by_id(post_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail='post not found')
        return PostGetResponseSchema(
            id=db_obj.id,
            creation_time=db_obj.creation_time.timestamp(),
            updated=(db_obj.updated_time.timestamp() if db_obj.updated_time
                     else None),
            creator=PostUserResponseSchema.from_sqlalchemy(db_obj.creator),
            name=db_obj.name,
            text=db_obj.text,
            media=[
                PostMediaResponseSchema.from_sqlalchemy(m)
                for m in db_obj.media
            ],
        )

    async def get(self,
                  offset=0,
                  limit=10,
                  created_after=0,
                  created_before=None,
                  **filters) -> List[PostGetResponseSchema]:
        if not created_before:
            created_before = aware_utcnow().timestamp()
        print("CREATED BEFORE", created_before)
        filters = {k: v for k, v in filters.items() if v is not None}
        db_objs = await PostRepository().select(
            custom_where=(and_(
                datetime.fromtimestamp(created_after) < Post.creation_time,
                Post.creation_time < datetime.fromtimestamp(created_before)
            )
            ),
            custom_offset=offset,
            custom_limit=limit,
            **filters
        )
        return [PostGetResponseSchema(
            id=db_obj.id,
            creation_time=db_obj.creation_time.timestamp(),
            updated=(
                db_obj.updated_time.timestamp() if db_obj.updated_time else None),
            creator=PostUserResponseSchema.from_sqlalchemy(db_obj.creator),
            name=db_obj.name,
            text=db_obj.text,
            media=[
                PostMediaResponseSchema.from_sqlalchemy(m)
                for m in db_obj.media
            ],
        )
            for db_obj in db_objs]

    async def delete(self, creator_id, post_id):
        db_obj = await PostRepository().get_by_id(post_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail='post not found')
        if creator_id != db_obj.creator_id:
            raise HTTPException(
                status_code=403,
                detail='user is not the post creator'
            )
        media = [
            PostMediaResponseSchema.from_sqlalchemy(m)
            for m in db_obj.media
        ]
        db_obj = await PostRepository().update(db_obj, media=[])
        db_obj = await PostRepository().delete(db_obj)
        return PostDeleteResponseSchema(
            id=db_obj.id,
            creation_time=db_obj.creation_time.timestamp(),
            updated=(
                db_obj.updated_time.timestamp() if db_obj.updated_time else None),
            name=db_obj.name,
            text=db_obj.text,
            media=media,
            creator=PostUserResponseSchema.from_sqlalchemy(db_obj.creator),
        )
