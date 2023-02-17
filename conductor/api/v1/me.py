from fastapi import APIRouter, Depends

from conductor.api.dependencies import get_current_user
from conductor.db.models import RoadmapDBM, UserDBM

me_router = APIRouter()


@me_router.get('.my_roadmap', response_model=RoadmapDBM)
async def my_roadmap():
    pass


@me_router.get('.my_profile', response_model=UserDBM)
async def my_profile(user: UserDBM = Depends(get_current_user)):
    return user
