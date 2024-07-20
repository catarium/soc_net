from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

from app.utils.response import Response
from app.services.auth import AuthService

router = APIRouter(prefix='/login')


class LoginSchema(BaseModel):
    name: str = Field(max_length=30)
    password: str = Field(max_length=50)


@router.post('')
async def login(request: Request, data: LoginSchema):
    res = await AuthService().check_password(request, data.name, data.password)
    return Response(res=res)
