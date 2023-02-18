from typing import Optional

from fastapi import APIRouter, Depends, Query
from fastapi import HTTPException, Body
from starlette import status

from conductor.api.dependencies import make_strict_depends_on_roles, get_current_user
from conductor.api.schemas.user import CreateUser, SensitiveUser, UpdateUser
from conductor.api.schemas.mailcode import OperationStatus
from conductor.core.misc import db, settings
from conductor.db.models import RoadmapDBM, UserDBM, Roles
from conductor.utils.send_mail import send_mail

user_router = APIRouter()


@user_router.post(".create", response_model=UserDBM)
async def create_user(
        user: UserDBM = Depends(make_strict_depends_on_roles(roles=[Roles.hr, Roles.supervisor])),
        user_to_create: CreateUser = Body()
):
    if user_to_create.role in (Roles.supervisor, Roles.hr) and user.role == Roles.hr:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='hr cant create supervisor or hr')

    roadmap_template = db.roadmap_template.get_document_by_int_id(user_to_create.roadmap_template_int_id)
    roadmap_template['created_by_int_id'] = user.int_id
    roadmap_template.pop('int_id', None)
    roadmap_template.pop('created', None)    

    roadmap = RoadmapDBM.parse_document(db.roadmap.insert_document(roadmap_template))

    to_create_dict = user_to_create.dict()
    to_create_dict.pop('roadmap_template_int_id')
    to_create_dict['roadmap_int_id'] = roadmap.int_id
    user_ = UserDBM(tokens=[], coins=0, **to_create_dict)
    inserted_user = UserDBM.parse_document(db.user.insert_document(user_.document()))

    send_mail(
        user_.email,
        f'Приглашение в кондукртор',
        f'Входите в систему Кондуктор https://divarteam.ru/ {settings.site_url}'
    )

    return inserted_user


@user_router.get('.by_int_id', response_model=Optional[SensitiveUser])
async def get_user_by_int_id(
        current_user=Depends(get_current_user),
        user_int_id: int = Query()
):
    user = db.user.get_document_by_int_id(user_int_id)
    if user is None:
        return None
    division = db.division.pymongo_collection.find_one({'int_id': user['division_int_id']})
    user['division_title'] = division['title']
    return SensitiveUser.parse_obj(user)


@user_router.get('', response_model=list[SensitiveUser])
async def get_users(
        current_user=Depends(get_current_user),
        division_int_id: Optional[int] = Query(None)
):
    if division_int_id is None:
        user_docs = db.user.get_all_docs()
    else:
        user_docs = db.user.pymongo_collection.find({'division_int_id': division_int_id})

    division_int_id_to_title = {}
    for division in db.division.pymongo_collection.find():
        division_int_id_to_title[division['int_id']] = division['title']

    res = []
    for user_doc in user_docs:
        user_doc['division_title'] = division_int_id_to_title[user_doc['division_int_id']]
        res.append(SensitiveUser.parse_obj(user_doc))
    return res


@user_router.get('.roles')
async def get_roles():
    return {'roles' : [Roles.employee, Roles.hr, Roles.supervisor]}
