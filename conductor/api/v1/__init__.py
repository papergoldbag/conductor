from fastapi import APIRouter

from conductor.api.v1 import echo
from conductor.api.v1 import routers

api_v1_router = APIRouter(prefix='/v1')
api_v1_router.include_router(echo.router, prefix='/echo', tags=['echo'])
api_v1_router.include_router(routers.users_router, prefix='/user', tags=['Users'])
api_v1_router.include_router(routers.roadmaps_router, prefix='/roadmap', tags=['Roadmaps'])
api_v1_router.include_router(routers.tasks_router, prefix='/tasks', tags=['Tasks'])
