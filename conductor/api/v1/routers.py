from fastapi import APIRouter

from conductor.core.misc import db
from conductor.api.schemas.common import *
from conductor.db.models import *

users_router = APIRouter()


@users_router.post('/')
async def create_user(user: CreateUser):
    ...


@users_router.get('/', response_model=UserByIdResponse)
async def get_user_by_id(user_id: int):
    user = db.user.pymongo_collection.find_one({'int_id' : user_id})
    if user is None:
        return UserByIdResponse(status=Statuses.BAD, out={}, err='user not found')
    user = User.parse_document(user)
    user_by_id = UserById.parse_obj(user)
    return UserByIdResponse(out={'user':user_by_id})


@users_router.get('/token/', response_model=UsersResponse)
async def get_user_by_token(user_token: str):
    user = db.user.pymongo_collection.find_one({'tokens' : {"$in" : [user_token,]}})
    if user is None:
        return UsersResponse(status=Statuses.BAD, out={}, err='user not found')
    user = User.parse_document(user)
    return UsersResponse(out={'user':user})


# TODO
@users_router.get('/roadmap/', response_model=RoadmapsResponse)
async def get_user_roadmap(user_id: int):
    user = db.user.pymongo_collection.find_one({'int_id' : user_id})
    print(user)
    if user is None:
        return UsersResponse(status=Statuses.BAD, out={}, err='user not found')
    user = User.parse_document(user)
    roadmap = db.roadmap.pymongo_collection.find_one({'int_id' : user.roadmap_int_id})
    if roadmap is None:
        return RoadmapsResponse(status=Statuses.BAD, out={}, err='roadmap not found')
    return roadmap


roadmaps_router = APIRouter()


@roadmaps_router.post('/')
async def create_roadmap(roadmap: CreateRoadmap):
    ...


# TODO
@roadmaps_router.get('/templates/', response_model=RoadmapsResponse)
async def get_template_roadmap(template_roadmap_id: int):
    roadmap_template = db.roadmap_templates.pymongo_collection.find_one({"int_id" : template_roadmap_id})
    if roadmap_template is None:
        return RoadmapsResponse(status=Statuses.BAD, out={}, err="roadmap template not found")
    roadmap_template = Roadmap.parse_document(roadmap_template)
    return RoadmapsResponse(out={'roadmap_template':roadmap_template})

tasks_router = APIRouter()


@tasks_router.post('/')
async def create_task(task: CreateTask):
    ...
