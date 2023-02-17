from pydantic import BaseModel

from conductor.api.schemas.base import BaseSchema
from conductor.db.models import UserDBM


class UserInOut(BaseModel):
    user: UserDBM


class UsersResponse(BaseSchema):
    out: UserInOut
