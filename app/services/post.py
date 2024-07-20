from typing import List

from fastapi import HTTPException
from pydantic import BaseModel

from app.db.repositories.post import PostRepository


class PostUserResponseSchema(BaseModel):
    id: int
    name: str


class PostCreateResponseSchema(BaseModel):
    id: int
    name: str
    text: str
    creator: PostUserResponseSchema


class PostGetResponseSchema(BaseModel):
    id: int
    name: str
    text: str
    creator: PostUserResponseSchema


class PostUpdateResponseSchema(BaseModel):
    id: int
    name: str
    text: str
    creator: PostUserResponseSchema


class PostDeleteResponseSchema(BaseModel):
    id: int
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
            name=db_obj.name,
            text=db_obj.text,
            creator=PostUserResponseSchema(
                id=db_obj.creator.id,
                name=db_obj.creator.name,
            )
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
            name=name,
            text=text
        )

        return PostUpdateResponseSchema(
            id=db_obj.id,
            name=db_obj.name,
            text=db_obj.text,
            creator=PostUserResponseSchema(
                id=db_obj.creator.id,
                name=db_obj.creator.name,
            )
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
            creator=PostUserResponseSchema(
                id=db_obj.creator.id,
                name=db_obj.creator.name),
            name=db_obj.name,
            text=db_obj.text
        )

    async def get(self, offset=0, limit=10, **filters) -> List[PostGetResponseSchema]:
        filters = {k: v for k, v in filters.items() if v is not None}
        db_objs = await PostRepository().select(
            custom_offset=offset,
            custom_limit=limit,
            **filters
        )
        return [PostGetResponseSchema(
            id=db_obj.id,
            creator=PostUserResponseSchema(
                id=db_obj.creator.id,
                name=db_obj.creator.name),
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
            name=db_obj.name,
            text=db_obj.text,
            creator=PostUserResponseSchema(
                id=db_obj.creator.id,
                name=db_obj.creator.name
            )
        )

