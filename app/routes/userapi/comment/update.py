from pydantic import BaseModel, model_validator
from fastapi import APIRouter, Request, Depends

from app.deps.auth.user_level import session_user
from app.services.comment import CommentService
from app.utils.response import Response

router = APIRouter(prefix='')


class CommentUpdateRequestSchema(BaseModel):
    comment_id: int
    text: str = None
    media: list[str] = None

    @model_validator(mode="after")
    def there_must_be_one(self):
        if not (self.text or self.media):
            raise ValueError("One parameter must be specified")
        return self


@router.put('/')
async def update(request: Request,
                 comment_schema: CommentUpdateRequestSchema,
                 user=Depends(session_user)):
    res = await CommentService().update(
        creator_id=user.id,
        **comment_schema.model_dump(exclude_none=True)
    )
    return Response(res=res)
