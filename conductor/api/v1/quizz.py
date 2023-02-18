from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Body
from starlette import status

from conductor.api.dependencies import get_strict_current_user
from conductor.api.schemas.quizz import SendAnswers
from conductor.api.schemas.roadmap import RoadmapResponse
from conductor.core.misc import db
from conductor.db.models import RoadmapDBM, UserDBM

quizz_router = APIRouter()


@quizz_router.post('.send_quizz', response_model=Optional[RoadmapDBM])
async def send_quizz(
        send_answers_: SendAnswers = Body(),
        current_user: UserDBM = Depends(get_strict_current_user),
):
    if current_user.roadmap_int_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user doesnt have roadmap')

    passed = 0
    roadmap = db.roadmap.get_document_by_int_id(current_user.roadmap_int_id)
    roadmap = RoadmapDBM.parse_obj(roadmap)
    task_type = roadmap.tasks[send_answers_.task_num].type 
    if task_type == 'hr_confirmation':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user cant answer hr confirmation task')
    for i in range(len(quizz:=roadmap.tasks[send_answers_.task_num].quizzes)):
        if quizz[i].correct_answer == send_answers_.answers[i]:
            passed+=1
        quizz[i].answer = send_answers_.answers[i]

    if passed >= len(roadmap.tasks[send_answers_.task_num].quizzes)//2:
        roadmap.tasks[send_answers_.task_num].is_completed = True

    return roadmap
