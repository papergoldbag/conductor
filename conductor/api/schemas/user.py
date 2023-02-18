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


class SensitiveUser(BaseModel):
    int_id: int
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
    division_title: str
