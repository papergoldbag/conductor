from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from conductor.db.models import Roles


class CreateUser(BaseModel):
    fullname: str
    email: EmailStr
    role: Roles
    position: str
    birth_date: datetime
    roadmap_int_id: Optional[int]
    division_int_id: int
