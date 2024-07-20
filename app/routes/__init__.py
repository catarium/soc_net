from fastapi import APIRouter
from .auth import router as auth_router
from .userapi import router as user_api_router
from .adminapi import router as admin_api_router


main_router = APIRouter()
main_router.include_router(auth_router)
main_router.include_router(user_api_router)
main_router.include_router(admin_api_router)
