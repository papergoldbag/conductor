from typing import Optional

from fastapi import APIRouter, Depends, Query
from fastapi import HTTPException, Body, Request, Header, Response, Cookie
from starlette import status
from conductor.api.schemas.mailcode import OperationStatus

from conductor.api.dependencies import get_current_user_token, make_strict_depends_on_roles, get_current_user
from conductor.api.schemas.user import CreateUser, SensitiveUser
from conductor.core.misc import db, settings
from conductor.db.models import UserDBM, Roles
from conductor.utils.send_mail import send_mail

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


@user_router.get('.by_int_id', response_model=Optional[SensitiveUser])
async def get_user_by_int_id(
        current_user=Depends(get_current_user),
        user_int_id: int = Query()
):
    user = db.user.get_document_by_int_id(user_int_id)
    if user is None:
        return None
    return SensitiveUser.parse_obj(user)


@user_router.get('', response_model=list[SensitiveUser])
async def get_users(
        current_user=Depends(get_current_user),
        division_int_id: Optional[int] = Query(None)
):
    if division_int_id is None:
        users = db.user.get_all_docs()
    else:
        users = db.user.pymongo_collection.find({'division_int_id': division_int_id})
    return [SensitiveUser.parse_obj(user) for user in users]




@user_router.get('.sign_out', response_model=OperationStatus)
async def signout(
     current_token: str = Depends(get_current_user_token),
     current_user: UserDBM = Depends(get_current_user)
    ):
    print(current_user)
    if current_user is None:
        return OperationStatus(is_done=False)
    tokens : list[str] = current_user.tokens
    tokens.remove(current_token)
    db.user.pymongo_collection.find_one_and_update({"int_id" : current_user.int_id}, {"$set" : {"tokens" : tokens}})
    return OperationStatus(is_done=True)
