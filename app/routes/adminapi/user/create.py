from typing import List

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

from app.services.user import UserService
from app.utils.response import Response

router = APIRouter(prefix='')


class UserCreateSchema(BaseModel):
    name: str = Field(max_length=30)
    password: str = Field(max_length=50)
    profile_picture: str 


@router.post('/',)
async def create(request: Request, user_schema: UserCreateSchema):
    res = await UserService().create(
        name=user_schema.name,
        password=user_schema.password,
        profile_picture=user_schema.profile_picture
    )
    return Response(user=res)

