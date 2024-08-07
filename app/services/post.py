from datetime import datetime
from typing import List

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import and_

from app.db.models import Post
from app.db.repositories.post import PostRepository
from app.utils.datetime_utils import aware_utcnow


class PostUserResponseSchema(BaseModel):
    id: int
    name: str

    @staticmethod
    def from_sqlalchemy(orm_model):
        return PostUserResponseSchema(
            id=orm_model.id,
            name=orm_model.name
        )


class PostCreateResponseSchema(BaseModel):
    id: int
    creation_time: float
    updated: float | None
    name: str
    text: str
    creator: PostUserResponseSchema


class PostGetResponseSchema(BaseModel):
    id: int
    creation_time: float
    updated: float | None
    name: str
    text: str
    creator: PostUserResponseSchema


class PostUpdateResponseSchema(BaseModel):
    id: int
    creation_time: float
    updated: float | None
    name: str
    text: str
    creator: PostUserResponseSchema


class PostDeleteResponseSchema(BaseModel):
    id: int
    creation_time: float
    updated: float | None
    name: str
    text: str
    creator: PostUserResponseSchema


class PostService:
    async def create(self, creator_id, name, text):
        db_obj = await PostRepository().create(
            creator_id=creator_id,
            name=name,
            text=text
        )
        return PostCreateResponseSchema(
            id=db_obj.id,
            creation_time=db_obj.creation_time.timestamp(),
            updated=(db_obj.updated_time.timestamp() if db_obj.updated_time else None),
            name=db_obj.name,
            text=db_obj.text,
            creator=PostUserResponseSchema.from_sqlalchemy(db_obj.creator)
        )

    async def update(self, creator_id, post_id, name, text):
        db_obj = await PostRepository().get_by_id(post_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail='post not found')
        if creator_id != db_obj.creator_id:
            raise HTTPException(
                status_code=403,
                detail='user is not the post creator'
            )
        await PostRepository().update(
            db_obj,
            creator_id=creator_id,
            updated_time=aware_utcnow().timestamp(),
            name=name,
            text=text
        )

        return PostUpdateResponseSchema(
            id=db_obj.id,
            creation_time=db_obj.creation_time.timestamp(),
            updated_time=db_obj.updated_time,
            updated=db_obj.updated_time.timestamp(),
            name=db_obj.name,
            text=db_obj.text,
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
            updated=(db_obj.updated_time.timestamp() if db_obj.updated_time else None),
            creator=PostUserResponseSchema.from_sqlalchemy(db_obj.creator),
            name=db_obj.name,
            text=db_obj.text
        )

    async def get(self,
                  offset=0,
                  limit=10,
                  created_after=0,
                  created_before=aware_utcnow().timestamp(),
                  **filters) -> List[PostGetResponseSchema]:
        filters = {k: v for k, v in filters.items() if v is not None}
        db_objs = await PostRepository().select(
            custom_where=(and_(datetime.fromtimestamp(created_after) < Post.creation_time, Post.creation_time < datetime.fromtimestamp(created_before)
                               )
                          ),
            custom_offset=offset,
            custom_limit=limit,
            **filters
        )
        return [PostGetResponseSchema(
            id=db_obj.id,
            creation_time=db_obj.creation_time.timestamp(),
            updated=(db_obj.updated_time.timestamp() if db_obj.updated_time else None),
            creator=PostUserResponseSchema.from_sqlalchemy(db_obj.creator),
            name=db_obj.name,
            text=db_obj.text)
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
        db_obj = await PostRepository().delete(db_obj)
        return PostDeleteResponseSchema(
            id=db_obj.id,
            creation_time=db_obj.creation_time.timestamp(),
            updated=(db_obj.updated_time.timestamp() if db_obj.updated_time else None),
            name=db_obj.name,
            text=db_obj.text,
            creator=PostUserResponseSchema.from_sqlalchemy(db_obj.creator),
        )

