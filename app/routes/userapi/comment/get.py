from typing import Optional

from fastapi import APIRouter, Request, Depends, HTTPException
from pydantic import BaseModel, model_validator, ValidationError, Field

from app.services.comment import CommentService
from app.utils.datetime_utils import aware_utcnow
from app.utils.response import Response

router = APIRouter(prefix='')


class CommentGetRequestSchema(BaseModel):
    id: Optional[int] = None
    post_id: Optional[int] = None
    creator_id: Optional[int] = None
    created_before: Optional[float] = None
    created_after: Optional[float] = 0
    offset: int = 0
    limit: int = Field(default=10, ge=1, le=30)

    @model_validator(mode="after")
    def there_must_be_one(self):
        if not (self.creator_id or self.post_id):
            raise HTTPException(
                status_code=422,
                detail="Either creator_id or post_id must be specified"
            )
        return self


@router.get('/')
async def get(request: Request,
              comment_schema: CommentGetRequestSchema = Depends()):
    res = await CommentService().get(
        **comment_schema.model_dump(exclude_none=True)
    )
    return Response(res=res)
