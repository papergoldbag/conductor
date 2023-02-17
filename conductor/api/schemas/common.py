from conductor.database.models import *


class Statuses:
    OK = 'OK'
    BAD = 'BAD'


class CommonResponse(BaseModel):
    status: str = Statuses.OK
    out: dict[str, Any]
    err: Optional[str] = None


class UsersResponse(CommonResponse):
    out: dict[str, User]


class RoadmapsResponse(CommonResponse):
    out: dict[str, Roadmap]
