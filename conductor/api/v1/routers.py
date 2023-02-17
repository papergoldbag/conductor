from fastapi import APIRouter

from conductor.api.schemas.common import *

users_router = APIRouter()


@users_router.post('/')
async def create_user(user: CreateUser):
    ...


# TODO
@users_router.get('/', response_model=UsersResponse)
async def get_user(user_id: int):
    ...


# TODO
@users_router.get('/roadmap/', response_model=RoadmapsResponse)
async def get_user_roadmap(user_id: int):
    ...


roadmaps_router = APIRouter()


@roadmaps_router.post('/')
async def create_roadmap(roadmap: CreateRoadmap):
    ...


# TODO
@roadmaps_router.get('/templates/', response_model=RoadmapsResponse)
async def get_template_roadmap(template_roadmap_id: int):
    ...


tasks_router = APIRouter()


@tasks_router.post('/')
async def create_task(task: CreateTask):
    ...
