from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateEvent(BaseModel):
    title: str
    desc: str
    dt: datetime
    division_int_id: Optional[int]
