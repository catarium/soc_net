from fastapi import APIRouter
from .create import router as router_create
# from .get import router as router_get
# from .delete import router as router_delete


router = APIRouter(
    prefix='/subscriber',
    tags=['userapi_subscriber']
)

router.include_router(router_create)
