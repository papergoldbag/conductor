from fastapi import APIRouter, Depends
from fastapi import HTTPException, Body
from starlette import status
from pydantic import BaseModel

from conductor.api.dependencies import make_strict_depends_on_roles
from conductor.api.schemas.user import CreateUser
from conductor.core.misc import db, settings
from conductor.db.models import UserDBM, Roles
from conductor.utils.send_mail import send_mail
from typing import Optional
from datetime import datetime

user_router = APIRouter()


@user_router.post(".create", response_model=UserDBM)
async def create_user(
        user: UserDBM = Depends(make_strict_depends_on_roles(roles=[Roles.hr, Roles.supervisor])),
        user_to_create: CreateUser = Body()
):
    if user_to_create.role in (Roles.supervisor, Roles.hr) and user.role == Roles.hr:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='hr cant create supervisor')
    user_ = UserDBM(tokens=[], coins=0, **user_to_create.dict())
    inserted = UserDBM.parse_document(db.user.insert_document(user_.document()))

    send_mail(user_.email, f'Приглашение', f'Входите в систему Кондуктор {settings.site_url}')

    return inserted


class SensetiveUser(BaseModel):
    fullname: str
    email: str
    role: Roles
    coins: int
    position: str
    birth_date: datetime
    telegram: Optional[str]
    whatsapp: Optional[str]
    vk: Optional[str]
    roadmap_int_id: Optional[int]
    division_int_id: int


@user_router.get('.by_int_id', response_model=SensetiveUser)
async def get_user_by_int_id(user_int_id: int):
    user = db.user.get_document_by_int_id(user_int_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
    return SensetiveUser.parse_obj(user)



@user_router.get('', response_model=list[SensetiveUser])
async def get_users(division_int_id: Optional[int] = None):
    if division_int_id is None:
        users = db.user.get_all_docs()
    else:
        users = db.user.pymongo_collection.find({'division_int_id': division_int_id})
    resp = []
    for user in users:
        resp.append(SensetiveUser.parse_obj(user))
    return resp
