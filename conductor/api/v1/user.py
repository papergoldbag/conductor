from fastapi import APIRouter, Depends

from conductor.api.dependencies import make_strict_depends_on_roles
from conductor.db.models import UserDBM, Roles
from conductor.api.schemas.user import CreateUser
from conductor.core.misc import db

user_router = APIRouter()


@user_router.post(".create")
def create_user(user: UserDBM = Depends(make_strict_depends_on_roles(roles=[Roles.hr, Roles.supervisor])), user_to_create: CreateUser = None):
    user = UserDBM(tokens=[], telegram='', whatsapp='', vk='', coins=0, **user_to_create.dict())
    inserted = UserDBM.parse_document(db.user.insert_document(user.document()))
    return inserted



