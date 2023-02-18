from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Body
from starlette import status

from conductor.api.dependencies import get_strict_current_user
from conductor.api.schemas.quizz import SendQuizz
from conductor.core.misc import db
from conductor.db.models import RoadmapDBM, UserDBM, TaskTypes

quizz_router = APIRouter()


@quizz_router.post('.send_quizz', response_model=Optional[RoadmapDBM])
async def send_quizz(
        send_quizz_: SendQuizz = Body(),
        current_user: UserDBM = Depends(get_strict_current_user),
):
    if current_user.roadmap_int_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user doesnt have any roadmap')

    passed = 0
    user_roadmap: RoadmapDBM = RoadmapDBM.parse_obj(db.roadmap.get_document_by_int_id(current_user.roadmap_int_id))

    if 0 > send_quizz_.task_num or send_quizz_.task_num >= len(user_roadmap.tasks):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no task num')
    task_type = user_roadmap.tasks[send_quizz_.task_num].type

    if len(user_roadmap.tasks[send_quizz_.task_num].quizzes) != len(send_quizz_.answers):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='bad len')

    if task_type == TaskTypes.hr_confirmation:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user cant answer hr confirmation task')

    for i in range(len(quizzes_ := user_roadmap.tasks[send_quizz_.task_num].quizzes)):
        if quizzes_[i].correct_answer.strip().lower() == send_quizz_.answers[i].strip().lower():
            passed += 1
        quizzes_[i].answer = send_quizz_.answers[i]

    if passed >= len(user_roadmap.tasks[send_quizz_.task_num].quizzes) // 2:
        user_roadmap.tasks[send_quizz_.task_num].is_completed = True

    db.roadmap.update_document_by_int_id(user_roadmap.int_id, user_roadmap.document())

    return user_roadmap
