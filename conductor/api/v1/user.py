from fastapi import APIRouter, Depends
from fastapi import HTTPException, Body
from starlette import status

from conductor.api.dependencies import make_strict_depends_on_roles
from conductor.db.models import UserDBM, Roles
from conductor.api.schemas.user import CreateUser
from conductor.core.misc import db

user_router = APIRouter()


@user_router.post(".create")
def create_user(user: UserDBM = Depends(make_strict_depends_on_roles(roles=[Roles.hr, Roles.supervisor])), user_to_create: CreateUser = None):
    if user_to_create.role in ('supervisor', 'hr') and user.role == 'hr':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='hr cant create supervisor')
    user_ = UserDBM(tokens=[], telegram='', whatsapp='', vk='', coins=0, **user_to_create.dict())
    inserted = UserDBM.parse_document(db.user.insert_document(user_.document()))
    return inserted



