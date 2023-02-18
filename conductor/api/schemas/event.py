from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class CreateEvent(BaseModel):
    title: str 
    desc: str
    dt: datetime
    division_int_id: Optional[int]
