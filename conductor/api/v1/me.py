from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from conductor.api.dependencies import get_current_user, get_strict_current_user
from conductor.api.schemas.roadmap import RoadmapResponse
from conductor.core.misc import db
from conductor.db.models import RoadmapDBM, UserDBM

me_router = APIRouter()


@me_router.get('.my_roadmap', response_model=Optional[RoadmapResponse])
async def my_roadmap(user: UserDBM = Depends(get_strict_current_user)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if user.roadmap_int_id is None:
        return {}
    roadmap_dbm = RoadmapDBM.parse_document(db.roadmap.get_document_by_int_id(user.roadmap_int_id))

    week_to_days = {}
    days = []
    weeks = []
    for task in roadmap_dbm.tasks:
        weeks.append(task.week_num)
        days.append(task.day_num)
        if task.week_num not in week_to_days:
            week_to_days[task.week_num] = []
        if task.day_num:
            week_to_days[task.week_num].append(task.day_num)

    data = roadmap_dbm.dict()

    return RoadmapResponse(
        weeks=list(sorted(set(weeks))),
        days=list(sorted(days)),
        week_to_days=week_to_days,
        **data
    )


@me_router.get('.my_profile', response_model=UserDBM)
async def my_profile(user: UserDBM = Depends(get_strict_current_user)):
    return user
