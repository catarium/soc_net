from datetime import datetime
from pprint import pprint
from typing import List

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import and_

from app.db.models import Post
from app.db.models.comment import Comment
from app.db.repositories.comment import CommentRepository
from app.db.repositories.media import MediaRepository
from app.db.repositories.post import PostRepository
from app.utils.datetime_utils import aware_utcnow, naive_utcnow


class CommentUserResponseSchema(BaseModel):
    id: int
    name: str

    @staticmethod
    def from_sqlalchemy(orm_model):
        return CommentUserResponseSchema(
            id=orm_model.id,
            name=orm_model.name
        )


class CommentPostResponseSchema(BaseModel):
    id: int
    creator: CommentUserResponseSchema
    name: str
    text: str

    @staticmethod
    def from_sqlalchemy(orm_model: Post):
        return CommentPostResponseSchema(
            id=orm_model.id,
            creator=CommentUserResponseSchema.from_sqlalchemy(
                orm_model.creator),
            name=orm_model.name,
            text=orm_model.text
        )


class CommentMediaResponseSchema(BaseModel):
    creator: CommentUserResponseSchema
    content_type: str
    filename: str

    @staticmethod
    def from_sqlalchemy(orm_model):
        return CommentMediaResponseSchema(
            creator=CommentUserResponseSchema.from_sqlalchemy(
                orm_model.creator),
            content_type=orm_model.content_type,
            filename=orm_model.filename
        )


class CommentCreateResponseSchema(BaseModel):
    id: int
    creation_time: float
    updated: float | None
    creator: CommentUserResponseSchema
    post: CommentPostResponseSchema
    text: str | None
    media: list[CommentMediaResponseSchema]


class CommentGetResponseSchema(BaseModel):
    id: int
    creation_time: float
    updated: float | None
    creator: CommentUserResponseSchema
    post: CommentPostResponseSchema
    text: str | None
    media: list[CommentMediaResponseSchema]


class CommentUpdateResponseSchema(BaseModel):
    id: int
    creation_time: float
    updated: float | None
    creator: CommentUserResponseSchema
    post: CommentPostResponseSchema
    text: str | None
    media: list[CommentMediaResponseSchema]


class CommentDeleteResponseSchema(BaseModel):
    id: int
    creation_time: float
    updated: float | None
    creator: CommentUserResponseSchema
    post: CommentPostResponseSchema
    text: str | None
    media: list[CommentMediaResponseSchema]


class CommentService:
    async def __check_post(self, post_id):
        post_obj = await PostRepository().get_by_id(post_id)
        if not post_obj:
            raise HTTPException(status_code=404, detail='post not found')

    async def create(self, creator_id, post_id, text, media):
        await self.__check_post(post_id)
        media_objs = []
        for m in media:
            m_obj = await MediaRepository().get_by_id(m)
            if not m_obj:
                raise HTTPException(
                    status_code=404,
                    detail=f'media not found: {m}'
                )
            media_objs.append(m_obj)
        db_obj = await CommentRepository().create(
            creator_id=creator_id,
            post_id=post_id,
            text=text,
            media=media_objs
        )
        return CommentCreateResponseSchema(
            id=db_obj.id,
            creation_time=db_obj.creation_time.timestamp(),
            updated=(
                db_obj.updated_time.timestamp() if db_obj.updated_time else None),
            creator=CommentUserResponseSchema.from_sqlalchemy(db_obj.creator),
            post=CommentPostResponseSchema.from_sqlalchemy(db_obj.post),
            text=db_obj.text,
            media=[
                CommentMediaResponseSchema.from_sqlalchemy(m)
                for m in db_obj.media
            ]
        )

    async def get(self,
                  offset=0,
                  limit=10,
                  created_after=0,
                  created_before=None,
                  **filters) -> List[CommentGetResponseSchema]:
        if not created_before:
            created_before = aware_utcnow().timestamp()
        db_objs = await CommentRepository().select(
            custom_where=(and_(
                datetime.fromtimestamp(created_after) < Comment.creation_time,
                Comment.creation_time < datetime.fromtimestamp(created_before)
            )
            ),
            custom_offset=offset,
            custom_limit=limit,
            **filters
        )
        pprint(db_objs)
        return [CommentGetResponseSchema(
            id=db_obj.id,
            creation_time=db_obj.creation_time.timestamp(),
            updated=(
                db_obj.updated_time.timestamp() if db_obj.updated_time else None),
            creator=CommentUserResponseSchema.from_sqlalchemy(db_obj.creator),
            post=CommentPostResponseSchema.from_sqlalchemy(db_obj.post),
            text=db_obj.text,
            media=[
                CommentMediaResponseSchema.from_sqlalchemy(m)
                for m in db_obj.media
            ]
        ) for db_obj in db_objs]

    async def update(self, creator_id, comment_id, **values):
        db_obj = await CommentRepository().get_by_id(comment_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail='comment not found')
        if db_obj.creator_id != creator_id:
            raise HTTPException(
                status_code=403,
                detail='user is not the comment creator'
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
            await CommentRepository().update(
                db_obj,
                media=[]
            )
        await CommentRepository().update(
            db_obj,
            updated_time=naive_utcnow(),
            **values
        )
        return CommentUpdateResponseSchema(
            id=db_obj.id,
            creation_time=db_obj.creation_time.timestamp(),
            updated=(
                db_obj.updated_time.timestamp() if db_obj.updated_time else None),
            creator=CommentUserResponseSchema.from_sqlalchemy(db_obj.creator),
            post=CommentPostResponseSchema.from_sqlalchemy(db_obj.post),
            text=db_obj.text,
            media=[
                CommentMediaResponseSchema.from_sqlalchemy(m)
                for m in db_obj.media
            ]
        )

    async def delete(self, creator_id, comment_id):
        db_obj = await CommentRepository().get_by_id(comment_id)
        if not db_obj:
            raise HTTPException(
                status_code=404,
                detail='comment not found'
            )
        if db_obj.creator_id != creator_id:
            raise HTTPException(
                status_code=403,
                detail='user is not the comment creator'
            )
        media = [
            CommentMediaResponseSchema.from_sqlalchemy(m)
            for m in db_obj.media
        ]
        db_obj = await CommentRepository().update(db_obj, media=[])
        db_obj = await CommentRepository().delete(db_obj)
        return CommentUpdateResponseSchema(
            id=db_obj.id,
            creation_time=db_obj.creation_time.timestamp(),
            updated=(
                db_obj.updated_time.timestamp() if db_obj.updated_time else None),
            creator=CommentUserResponseSchema.from_sqlalchemy(db_obj.creator),
            post=CommentPostResponseSchema.from_sqlalchemy(db_obj.post),
            text=db_obj.text,
            media=media
        )
