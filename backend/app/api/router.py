from fastapi import APIRouter

from app.api.v1 import auth
from app.api.v1 import health
from app.api.v1 import items
from app.api.v1 import recommendations

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
