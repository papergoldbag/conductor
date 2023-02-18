from fastapi import APIRouter, Depends
from pydantic import BaseModel

from conductor.api.dependencies import make_strict_depends_on_roles
from conductor.api.schemas.roadmap_template import CreateRoadmapTemplate
from conductor.db.models import RoadmapDBM, UserDBM, Roles, TaskDBM
from conductor.core.misc import db

roadmap_template_router = APIRouter()


@roadmap_template_router.get('', response_model=list[RoadmapDBM])
async def get_all_roadmap_templates(
    user: UserDBM = Depends(make_strict_depends_on_roles(roles=[Roles.hr, Roles.supervisor]))
):
    templates = db.roadmap_template.get_all_docs()
    return [RoadmapDBM.parse_document(x) for x in templates]


class MiniRoadmapTemplate(BaseModel):
    int_id: int
    title: str


@roadmap_template_router.get('.mini', response_model=list[MiniRoadmapTemplate])
async def get_mini_roadmap_templates(
    user: UserDBM = Depends(make_strict_depends_on_roles(roles=[Roles.hr, Roles.supervisor]))
):
    templates = db.roadmap_template.get_all_docs()
    return [MiniRoadmapTemplate.parse_obj(x) for x in templates]


@roadmap_template_router.get('.create', deprecated=True)
async def create_roadmap_template(
        roadmap_template_to_create: CreateRoadmapTemplate,
        user: UserDBM = Depends(make_strict_depends_on_roles(roles=[Roles.hr, Roles.supervisor]))
):
    roadmap_template_dbm = RoadmapDBM(
        title=roadmap_template_to_create.title,
        tasks=[
            TaskDBM(
                type=task.type,
                title=task.type,
                text=task.text,
                is_confirmed_by_hr_int_id=False,
                coins=task.coins,
                is_completed=False,
                week_num=task.week_num,
                day_num=task.day_num,
                attachments=task.attachments,
                quizzes=task.quizzes
            ) for task in roadmap_template_to_create.tasks
        ],
        created_by_int_id=user.int_id
    )
    print(roadmap_template_dbm)
