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
    day_to_tasks = {}
    for task in roadmap_dbm.tasks:
        weeks.append(task.week_num)
        days.append(task.day_num)
        if task.week_num not in week_to_days:
            week_to_days[task.week_num] = []
        if task.day_num:
            week_to_days[task.week_num].append(task.day_num)
        if task.day_num not in day_to_tasks:
            day_to_tasks[task.day_num] = []
        day_to_tasks[task.day_num].append(task)

    #  dict[int, dict[int, list[TaskDBM]]]
    easy_view = {}
    for week, days in week_to_days.items():
        easy_view[week] = {}
        for day in days:
            easy_view[week][day] = []
            for task in day_to_tasks[day]:
                easy_view[week][day].append(task)

    easy_view2 = {'weeks': []}
    for week, days in week_to_days.items():
        to_append = {'week': week, 'days': []}
        for day in week_to_days[week]:
            to_append['days'].append({'day': day, 'tasks': []})
            for task in day_to_tasks[day]:
                to_append['days'][-1]['tasks'].append(task)
        easy_view2['weeks'].append(to_append)

    data = roadmap_dbm.dict()

    return RoadmapResponse(
        weeks=list(sorted(set(weeks))),
        days=list(sorted(days)),
        week_to_days=week_to_days,
        easy_view=easy_view,
        easy_view2=easy_view2,
        **data
    )


@me_router.get('.my_profile', response_model=UserDBM)
async def my_profile(user: UserDBM = Depends(get_strict_current_user)):
    return user
