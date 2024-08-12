from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel, Field, validator, model_validator, \
    ValidationError

from app.deps.auth.user_level import session_user
from app.services.post import PostService
from app.services.user import UserService
from app.utils.response import Response

router = APIRouter(prefix='')


class PostCreateRequestSchema(BaseModel):
    name: str = Field(max_length=120)
    text: str = None
    media: list[str] = None

    @model_validator(mode="after")
    def there_must_be_one(self):
        if not (self.text or self.media):
            raise ValueError("One parameter must be specified")
        return self


@router.post('/',)
async def create(request: Request,
                 post_schema: PostCreateRequestSchema,
                 user=Depends(session_user)
                 ):
    res = await PostService().create(
        name=post_schema.name,
        text=post_schema.text,
        creator_id=user.id,
        media=post_schema.media
    )
    return Response(res=res)