from datetime import date, datetime

from pydantic import BaseModel


class User(BaseModel):
    int_id : int
    email: str
    tokens: list[str]
    role: str
    coins: int
    position: str
    birth_date: date
    description: str
    telegram: str
    whatsapp: str
    vk: str
    roadmap_int_id: str
    division_int_id: str


class Test(BaseModel):
    question: str
    answer: str
    correct: str


class Task(BaseModel):
    id: int
    type: str
    title: str
    text: str
    attachments: dict[str, str]
    test: list[Test]
    marked_by_hr_id: str
    coins: int
    is_completed: bool


class Roadmap(BaseModel):
    id: int
    created: datetime
    title: str
    tasks: dict[int, Task]
    created_by_id: str
