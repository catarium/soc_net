from fastapi import APIRouter
from .create import router as router_create
from .get import router as router_get


router = APIRouter(
    prefix='/user',
    tags=['adminapi_user']
)
router.include_router(router_create)
router.include_router(router_get)