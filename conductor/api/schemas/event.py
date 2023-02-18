from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class CreateEvent(BaseModel):
    title: str 
    desc: str
    dt: datetime
    to_user_int_ids: Optional[list[int]]
    division_int_id: Optional[int]