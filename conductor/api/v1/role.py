from fastapi import APIRouter
from pydantic import BaseModel

from conductor.db.models import Roles


role_router = APIRouter()


class RolesResponseSchema(BaseModel):
    roles: list[str]


@role_router.get('.roles', response_model=RolesResponseSchema)
async def get_roles():
    return RolesResponseSchema(roles=[Roles.employee, Roles.hr, Roles.supervisor])