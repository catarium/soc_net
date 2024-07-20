from fastapi import APIRouter, Depends

from app.deps.auth.admin_level import session_admin
from app.routes.adminapi.user import router as user_router


router = APIRouter(prefix='/adminapi', dependencies=[Depends(session_admin)])
router.include_router(user_router)