from fastapi import APIRouter
from conductor.api.schemas.common import *
from datetime import date

users_router = APIRouter()


@users_router.get('/', response_model=UsersResponse)
async def get_user(id : str):
    ...

@users_router.post('/', response_model=UsersResponse)
async def create_user(user : User):
    ...


roadmaps_router = APIRouter()


@roadmaps_router.get('/', response_model=RoadmapsResponse)
async def get_roadmap(id : str):
    ...

@roadmaps_router.post('/', response_model=RoadmapsResponse)
async def create_new_roadmap(roadmap : Roadmap):
    ...

@roadmaps_router.post('/', response_model=TasksResponse)
async def get_roadmap_tasks(id : str):
    ...