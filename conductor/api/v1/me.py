from fastapi import APIRouter

from conductor.api.schemas.roadmap import RoadmapResponse
from conductor.api.schemas.user import UsersResponse

me_router = APIRouter()


@me_router.get('.my_roadmap', response_model=RoadmapResponse)
async def get_template_roadmap():
    pass


@me_router.get('.my_profile', response_model=UsersResponse)
async def get_template_roadmap():
    pass
