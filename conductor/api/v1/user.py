from fastapi import APIRouter, Depends
from fastapi import HTTPException, Body
from starlette import status

from conductor.api.dependencies import make_strict_depends_on_roles
from conductor.api.schemas.user import CreateUser
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


@user_router.get('.by_int_id')
async def get_user_by_int_id():
    pass


@user_router.get('')
async def get_users():
    pass
