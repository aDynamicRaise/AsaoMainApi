from fastapi import APIRouter

from config import settings
from auth.routers import user_router
from statistics.router import router as stats_router


router = APIRouter(
    prefix = settings.api.prefix,
)

router.include_router(
    user_router,
    prefix=settings.api.users, 
)

router.include_router(
    stats_router,
    prefix=settings.api.stats,
)