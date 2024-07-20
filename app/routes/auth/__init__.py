from fastapi import APIRouter
from .login import router as router_login
from .registration import router as router_registration
from .me import router as router_me

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)
router.include_router(router_login)
router.include_router(router_registration)
router.include_router(router_me)
