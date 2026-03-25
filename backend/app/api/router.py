# Central API router — aggregates all v1 endpoint routers.
from fastapi import APIRouter

from app.api.v1.jobs import router as jobs_router
from app.api.v1.platforms import router as platforms_router

api_router = APIRouter()
api_router.include_router(jobs_router)
api_router.include_router(platforms_router)
