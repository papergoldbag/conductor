from fastapi import APIRouter

from conductor.api.schemas.common import *

users_router = APIRouter()


@users_router.get('/', response_model=UsersResponse)
async def get_user(user_id: int):
    ...


@users_router.get('/roadmap/', response_model=RoadmapsResponse)
async def get_user_roadmap(user_id: int):
    ...


roadmaps_router = APIRouter()


@roadmaps_router.get('/', response_model=RoadmapsResponse)
async def get_template_roadmap(template_roadmap_id: int):
    ...
