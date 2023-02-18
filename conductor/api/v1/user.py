from fastapi import APIRouter, Depends

from conductor.api.dependencies import make_strict_depends_on_roles
from conductor.db.models import UserDBM, Roles

user_router = APIRouter()


@user_router.post(".create")
def create_user(user: UserDBM = Depends(make_strict_depends_on_roles(roles=[Roles.hr, Roles.supervisor]))):
    return {}
