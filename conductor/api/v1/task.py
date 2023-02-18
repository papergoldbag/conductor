from fastapi import APIRouter, Depends, HTTPException, Query
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

    doc = db.roadmap.get_document_by_int_id(current_user.roadmap_int_id)
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user doesnt have this roadmap')

    roadmap = RoadmapDBM.parse_document(doc)
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
    user = db.user.get_document_by_int_id(user_int_id)
    if user is None:
        return None
    user = UserDBM.parse_document(user)
    if user.roadmap_int_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user doesnt have any roadmap')

    doc = db.roadmap.get_document_by_int_id(user.roadmap_int_id)
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user doesnt have this roadmap')

    roadmap = RoadmapDBM.parse_document(doc)
    tasks = roadmap.tasks
    task = None
    for t in tasks:
        if t.index == task_index:
            task = t
            task.is_completed = True
        
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user doesnt have task with this index in roadmap')
                
    db.roadmap.pymongo_collection.find_one_and_update({'int_id' : roadmap.int_id}, {'$set' : {'tasks': [t.dict() for t in tasks]}})

    return True