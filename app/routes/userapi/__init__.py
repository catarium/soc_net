from fastapi import APIRouter, Depends

from app.deps.auth.user_level import session_user
from app.routes.userapi.test import router as test_router
from app.routes.userapi.post import router as post_router
from app.routes.userapi.user import router as user_router
from app.routes.userapi.subscriber import router as subscriber_router


router = APIRouter(prefix='/userapi', dependencies=[Depends(session_user)])
router.include_router(test_router)
router.include_router(post_router)
router.include_router(user_router)
router.include_router(subscriber_router)