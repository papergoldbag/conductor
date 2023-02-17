from fastapi import APIRouter

from conductor.api.v1 import echo
from conductor.api.v1 import routers

api_v1_router = APIRouter(prefix='/v1')
api_v1_router.include_router(echo.router, prefix='/echo')
api_v1_router.include_router(routers.users_router, prefix='/user')
api_v1_router.include_router(routers.roadmaps_router, prefix='/roadmap')
