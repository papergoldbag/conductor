from fastapi import APIRouter

from conductor.api.v1 import auth, echo, me
from conductor.api.v1.auth import auth_router
from conductor.api.v1.divisions import division_router
from conductor.api.v1.echo import echo_router
from conductor.api.v1.me import me_router

api_v1_router = APIRouter(prefix='/v1')
api_v1_router.include_router(echo_router, prefix='/echo', tags=['echo'])
api_v1_router.include_router(auth_router, prefix='/auth', tags=['auth'])
api_v1_router.include_router(me_router, prefix='/me', tags=['me'])
api_v1_router.include_router(division_router, prefix='/divisions', tags=['divisions'])
# api_v1_router.include_router(users_router, prefix='/user', tags=['Users'])
# api_v1_router.include_router(roadmaps_router, prefix='/roadmap', tags=['Roadmaps'])
# api_v1_router.include_router(authentication.router, prefix='/auth', tags=['Auth'])
