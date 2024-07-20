from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

from app.utils.response import Response
from app.services.auth import AuthService

router = APIRouter(prefix='/registration')


class RegistrationSchema(BaseModel):
    name: str = Field(max_length=30)
    password: str = Field(max_length=50)


@router.post('')
async def registration(request: Request, data: RegistrationSchema):
    user_response = await AuthService().register_user(
        request,
        name=data.name,
        password=data.password
    )
    return Response(res=user_response)
