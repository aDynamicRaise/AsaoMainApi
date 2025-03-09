from fastapi import APIRouter

from config import settings
from auth.routers import router as router_users


router = APIRouter(
    prefix = settings.api.prefix,
)

router.include_router(
    router_users,
    prefix=settings.api.users, 
)