from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from conductor.api.dependencies import get_strict_current_user, make_strict_depends_on_roles
from conductor.core.misc import db
from conductor.db.models import RoadmapDBM, Roles, UserDBM, TaskDBM

task_router = APIRouter()


@task_router.get('.week_day_tasks', response_model=list[TaskDBM])
async def get_tasks_by_week_day(
        week_num: int,
        day_num: int,
        current_user: UserDBM = Depends(get_strict_current_user)
):
    if current_user.roadmap_int_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user doesnt have any roadmap')

    roadmap_doc = db.roadmap.get_document_by_int_id(current_user.roadmap_int_id)
    if roadmap_doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user doesnt have this roadmap')

    roadmap = RoadmapDBM.parse_document(roadmap_doc)
    tasks_for_week_day = []
    for t in roadmap.tasks:
        if t.week_num == week_num and t.day_num == day_num:
            tasks_for_week_day.append(t)

    return tasks_for_week_day


@task_router.get(".confirmation")
async def make_confirmation(
        user_int_id: int,
        task_index: int,
        current_user: UserDBM = Depends(make_strict_depends_on_roles(roles=[Roles.hr, Roles.supervisor]))
):
    user_doc = db.user.get_document_by_int_id(user_int_id)
    if user_doc is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'no user with id={user_int_id}')

    user: UserDBM = UserDBM.parse_document(user_doc)

    user_roadmap_doc = db.roadmap.get_document_by_int_id(user.roadmap_int_id)
    if user_roadmap_doc is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user doesnt have this roadmap')
    user_roadmap = RoadmapDBM.parse_document(user_roadmap_doc)

    tasks = user_roadmap.tasks
    found_task = None
    for t in tasks:
        if t.index == task_index:
            found_task = t
            found_task.is_completed = True
            found_task.is_confirmed_by_int_id = current_user.int_id

    if found_task is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='user doesnt have task with this index in roadmap')

    db.roadmap.pymongo_collection.find_one_and_update(
        {'int_id': user_roadmap.int_id},
        {'$set': {'tasks': [t.dict() for t in tasks]}}
    )

    to_user = UserDBM.parse_document(user_doc)
    db.user.update_document_by_int_id(
        to_user.int_id,
        {'coins': to_user.coins + found_task.coins}
    )

    return True
