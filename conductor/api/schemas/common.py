from conductor.database.models import *
from typing import Any, Optional


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


class CreateUser(BaseModel):
    email: str
    role: str
    position: str
    birth_date: date
    description: str
    telegram: str
    whatsapp: str
    vk: str
    roadmap_id: Optional[int]
    division_id: int


class CreateRoadmap(BaseModel):
    title: str
    tasks: dict[int, Task]
    created_by_id: str


class Test(BaseModel):
    question: str
    answer: str
    correct: str


class CreateTask(BaseModel):
    type: str
    title: str
    text: str
    attachments: dict[str, str]
    test: list[Test]
    coins: int


