from typing import Any, Optional

from pydantic import BaseModel


class Statuses:
    OK = 'OK'
    BAD = 'BAD'


class CommonResponse(BaseModel):
    status: str = Statuses.OK
    out: dict[str, Any]
    err: Optional[str] = None
