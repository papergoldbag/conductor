from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status

from conductor.api.dependencies import get_current_user
from conductor.api.dependencies import get_strict_current_user
from conductor.api.schemas.mailcode import OperationStatus
from conductor.api.schemas.roadmap import RoadmapResponse
from conductor.api.schemas.user import UpdateUser, UserDBMWithDivision
from conductor.core.misc import db
from conductor.db.models import RoadmapDBM, UserDBM, TaskDBM, EventDBM, DivisionDBM, ProductDBM

me_router = APIRouter()


@me_router.get('.my_roadmap', response_model=Optional[RoadmapResponse])
async def my_roadmap(user: UserDBM = Depends(get_strict_current_user)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if user.roadmap_int_id is None:
        return None
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
                if task.week_num != week:
                    continue
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


@me_router.patch('', response_model=OperationStatus)
async def change_user_contacts(
        contacts: UpdateUser,
        current_user: UserDBM = Depends(get_current_user)
):
    _user = current_user.document()
    for k, v in contacts:
        _user[k] = v
    db.user.update_document_by_int_id(current_user.int_id, _user)
    return OperationStatus(is_done=True)


@me_router.get('.my_profile', response_model=UserDBMWithDivision)
async def my_profile(user: UserDBM = Depends(get_strict_current_user)):
    division = db.division.get_document_by_int_id(user.division_int_id)
    data = user.dict()
    data['division_title'] = division['title']
    user_with_division = UserDBMWithDivision.parse_obj(data)
    return user_with_division


@me_router.get('.division', response_model=DivisionDBM)
async def my_profile(user: UserDBM = Depends(get_strict_current_user)):
    division_doc = db.division.get_document_by_int_id(user.division_int_id)
    return DivisionDBM.parse_document(division_doc)


@me_router.get('.get_task_by_index', response_model=Optional[TaskDBM])
async def get_task_by_index(
        task_index: int = Query(),
        current_user: UserDBM = Depends(get_strict_current_user),
):
    if current_user.roadmap_int_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user doesnt have any roadmap')

    roadmap_doc = db.roadmap.get_document_by_int_id(current_user.roadmap_int_id)
    if roadmap_doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user doesnt have this roadmap')

    roadmap = RoadmapDBM.parse_document(roadmap_doc)
    for task in roadmap.tasks:
        if task.index == task_index:
            return task
    return None


@me_router.get('.get_my_events', response_model=list[EventDBM])
async def get_my_events(
        current_user: UserDBM = Depends(get_strict_current_user),
):
    events = db.event.pymongo_collection.find({'division_int_id': {'$in': [current_user.division_int_id]}})
    return [EventDBM.parse_document(event) for event in events]


# def define_progress(user_int_id: int) -> int:
#     user = UserDBM.parse_document(db.user.pymongo_collection.find_one({'int_id': user_int_id}))
#     if user.roadmap_int_id is None:
#         raise 0
#
#     roadmap_of_user = RoadmapDBM.parse_document(db.roadmap.get_document_by_int_id(user.roadmap_int_id))
#     len_tasks = len(roadmap_of_user.tasks)
#     done = 0
#     for task in roadmap_of_user.tasks:
#         if task.is_completed:
#             if task.is_good is not None:
#                 pass
#             elif task.is_good is True:
#                 pass
#             else:
#                 pass


@me_router.get('.progress')
async def progress():
    pass


@me_router.get('.my_products', response_model=list[ProductDBM])
async def my_products(
        current_user: UserDBM = Depends(get_strict_current_user)
):
    res = []
    for product_doc in db.user.get_all_docs():
        if product_doc['int_id'] in current_user.purchased_product_int_ids:
            res.append(ProductDBM.parse_document(product_doc))
    return res
