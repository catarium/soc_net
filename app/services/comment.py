from pydantic import BaseModel

from app.db.models import Post
from app.db.repositories.comment import CommentRepository


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
            creator=CommentUserResponseSchema.from_sqlalchemy(orm_model.creator),
            name=orm_model.name,
            text=orm_model.text
        )


class CommentCreateResponseSchema(BaseModel):
    id: int
    creator: CommentUserResponseSchema
    post: CommentPostResponseSchema
    text: str


class CommentGetResponseSchema(BaseModel):
    id: int
    creator: CommentUserResponseSchema
    post: CommentPostResponseSchema
    text: str


class CommentService:
    async def create(self, creator_id, post_id, text):
        db_obj = await CommentRepository().create(
            creator_id=creator_id,
            post_id=post_id,
            text=text
        )
        return CommentCreateResponseSchema(
            id=db_obj.id,
            creator=CommentUserResponseSchema.from_sqlalchemy(db_obj.creator),
            post=CommentPostResponseSchema.from_sqlalchemy(db_obj.post),
            text=db_obj.text
        )

    async def get_by_id(self, comment_id):
        db_obj = await CommentRepository().get_by_id(comment_id)
        return CommentGetResponseSchema(
            id=db_obj.id,
            creator=CommentUserResponseSchema.from_sqlalchemy(db_obj.creator),
            post=CommentPostResponseSchema.from_sqlalchemy(db_obj.post),
            text=db_obj.text
        )

