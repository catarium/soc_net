from fastapi import APIRouter
from .get import router_get

router = APIRouter(
    prefix='/test',
    tags=['userapi_test']
)
router.include_router(router_get)
