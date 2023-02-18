from fastapi import APIRouter

from conductor.api.v1 import auth, echo, me
from conductor.api.v1.auth import auth_router
from conductor.api.v1.divisions import division_router
from conductor.api.v1.echo import echo_router
from conductor.api.v1.me import me_router
from conductor.api.v1.quizz import quizz_router
from conductor.api.v1.roadmap_template import roadmap_template_router
from conductor.api.v1.user import user_router

api_v1_router = APIRouter(prefix='/v1')
api_v1_router.include_router(echo_router, prefix='/echo', tags=['echo'])
api_v1_router.include_router(auth_router, prefix='/auth', tags=['auth'])
api_v1_router.include_router(me_router, prefix='/me', tags=['me'])
api_v1_router.include_router(division_router, prefix='/divisions', tags=['divisions'])
api_v1_router.include_router(user_router, prefix='/user', tags=['Users'])
api_v1_router.include_router(roadmap_template_router, prefix='/roadmap_template', tags=['Roadmap Templates'])
api_v1_router.include_router(quizz_router, prefix='/send_answers', tags=['Send Answers'])
# api_v1_router.include_router(roadmaps_router, prefix='/roadmap', tags=['Roadmaps'])
# api_v1_router.include_router(authentication.router, prefix='/auth', tags=['Auth'])
