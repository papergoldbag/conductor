from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel


class Statuses(str, Enum):
    OK = 'OK'
    BAD = 'BAD'


class BaseSchema(BaseModel):
    status: str = Statuses.OK
    out: dict[str, Any] = {}
    err: Optional[str] = None
