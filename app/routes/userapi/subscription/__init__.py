from fastapi import APIRouter
from .create import router as router_create
from .get import router as router_get
from .delete import router as router_delete


router = APIRouter(
    prefix='/subscription',
    tags=['userapi_subscription']
)

router.include_router(router_create)
router.include_router(router_delete)
router.include_router(router_get)
