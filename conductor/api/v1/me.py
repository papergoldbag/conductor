from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from conductor.api.dependencies import get_current_user
from conductor.core.misc import db
from conductor.db.models import RoadmapDBM, UserDBM

me_router = APIRouter()


@me_router.get('.my_roadmap', response_model=Optional[RoadmapDBM])
async def my_roadmap(user: UserDBM = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if user.roadmap_int_id is None:
        return {}
    roadmap = RoadmapDBM.parse_document(db.roadmap.get_document_by_int_id(user.roadmap_int_id))
    return roadmap


@me_router.get('.my_profile', response_model=UserDBM)
async def my_profile(user: UserDBM = Depends(get_current_user)):
    return user
