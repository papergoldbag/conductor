from fastapi import APIRouter

from conductor.api.v1 import echo

api_v1_router = APIRouter(prefix='/v1')
api_v1_router.include_router(echo.router, prefix='/echo')
