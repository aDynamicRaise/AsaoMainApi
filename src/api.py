from fastapi import APIRouter

from config import settings
from auth.routers import user_router
from statists.router import router as stats_router
from collecting.router import router as collecting_router
from forecast.router import router as forecast_router



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

router.include_router(
    collecting_router,
    prefix=settings.api.collecting,
)

router.include_router(
    forecast_router,
    prefix=settings.api.forecast,
)