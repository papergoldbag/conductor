from typing import Any, Optional
from datetime import date

from pydantic import BaseModel


class Statuses:
    OK = 'OK'
    BAD = 'BAD'


class CommonResponse(BaseModel):
    status: str = Statuses.OK
    out: dict[str, Any]
    err: Optional[str] = None

class User(BaseModel):
    id : str
    email : str
    tokens : list[str]
    role : str
    coins : int
    position : str
    birth_date : date
    description : str
    telegram : str
    whatsapp : str
    vk : str
    roadmap_id : str
    division_id : str


class UsersResponse(CommonResponse):
    out : dict[str, User]


class Task(BaseModel):
    id : str
    type : str
    title : str
    text : str
    attachments : list[str]
    test : list[dict[str, str]]
    marked_completed_by_id : str
    coins : int


class TasksResponse(CommonResponse):
    out : dict[str, Task]


class Roadmap(BaseModel):
    id : str
    title : str
    tasks : list[Task]
    created_by_id : str


class RoadmapsResponse(CommonResponse):
    out : dict[str, Roadmap]

