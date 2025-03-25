from fastapi import APIRouter

from config import settings
from auth.routers import user_router


router = APIRouter(
    prefix = settings.api.prefix,
)

router.include_router(
    user_router,
    prefix=settings.api.users, 
)