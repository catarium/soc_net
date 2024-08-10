from fastapi import APIRouter, Request, Depends, UploadFile, HTTPException
from pydantic import BaseModel, Field

from app.db.repositories.media import MediaRepository
from app.deps.auth.user_level import session_user
from app.services.media import MediaService
from app.services.post import PostService
from app.services.user import UserService
from app.utils.response import Response

router = APIRouter(prefix='')


@router.post('/',)
async def create(request: Request,
                 files: list[UploadFile],
                 user=Depends(session_user)
                 ):
    allowed_content_types = (
        'image',
        'video',
        'audio',
    )
    print(files[0])
    for file in files:
        if file.content_type.split('/')[0] not in allowed_content_types:
            raise HTTPException(status_code=400)
    res = [(await MediaService().create(file.file,
                                 user.id,
                                 file.content_type))
           for file in files]
    return Response(res=res)
