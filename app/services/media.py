from typing import BinaryIO

from pydantic import BaseModel

from app.db.repositories.media import MediaRepository
from uuid import uuid4


class MediaUserResponseSchema(BaseModel):
    id: int
    name: str

    @staticmethod
    def from_sqlalchemy(orm_model):
        return MediaUserResponseSchema(
            id=orm_model.id,
            name=orm_model.name
        )


class MediaCreateResponseSchema(BaseModel):
    creator: MediaUserResponseSchema
    content_type: str
    filename: str


class MediaService:
    async def create(self,
                     file_obj: BinaryIO,
                     creator_id: int,
                     content_type: str
                     ):
        filename = f'{uuid4().hex}.{content_type.split("/")[1]}'
        db_obj = await MediaRepository().create(
            creator_id=creator_id,
            content_type=content_type,
            filename=filename
        )
        with open(f'static/images/{filename}', 'wb') as f:
            f.write(file_obj.read())
        return MediaCreateResponseSchema(
            creator=MediaUserResponseSchema.from_sqlalchemy(db_obj.creator),
            content_type=db_obj.content_type,
            filename=db_obj.filename
        )
