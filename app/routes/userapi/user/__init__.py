from fastapi import APIRouter
from .get import router as router_get


router = APIRouter(
    prefix='/user',
    tags=['userapi_user']
)
router.include_router(router_get)