from fastapi import APIRouter
from .create import router as router_create
# from .get import router as router_get
# from .update import router as router_update
# from .delete import router as router_delete


router = APIRouter(
    prefix='/media',
    tags=['userapi_media']
)
router.include_router(router_create)
# router.include_router(router_get)
# router.include_router(router_update)
# router.include_router(router_delete)

