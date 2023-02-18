from fastapi import APIRouter

from conductor.db.models import Roles


role_router = APIRouter()


@role_router.get('.roles')
async def get_roles():
    return {'roles' : [Roles.employee, Roles.hr, Roles.supervisor]}