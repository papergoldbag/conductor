from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from conductor.db.base import BaseInDB, Document


class DivisionDBM(BaseInDB):
    title: str


class Roles(str, Enum):
    hr = 'hr'
    supervisor = 'supervisor'
    employee = 'employee'


class UserDBM(BaseInDB):
    fullname: str
    email: str
    tokens: list[str] = []
    role: Roles
    coins: int
    position: str
    birth_date: datetime
    telegram: Optional[str] = None
    whatsapp: Optional[str] = None
    vk: Optional[str] = None
    roadmap_int_id: Optional[int] = None
    division_int_id: int
    purchased_product_int_ids: list[int] = []

    def document(self) -> Document:
        doc = super().document()
        doc['role'] = self.role.value
        return doc


class QuizDBM(BaseModel):
    question: str
    answer: Optional[str]
    correct_answer: Optional[str]


class TaskTypes(str, Enum):
    auto_test = 'auto_test'
    hr_confirmation = 'hr_confirmation'
    feedback = 'feedback'


class Attachment(BaseModel):
    title: str
    url: str


class TaskDBM(BaseModel):
    index: int
    type: TaskTypes
    title: str
    text: str
    is_confirmed_by_int_id: Optional[int]
    coins: int
    is_completed: bool
    is_good: Optional[bool]
    week_num: int
    day_num: int
    attachments: list[Attachment]
    quizzes: list[QuizDBM]

    def dict(self, *args, **kwargs):
        doc = super().dict(*args, **kwargs)
        doc['type'] = self.type.value
        return doc


class RoadmapDBM(BaseInDB):
    title: str
    tasks: list[TaskDBM]
    created_by_int_id: int


class MailCodeDBM(BaseInDB):
    mail: str
    code: int


class EventDBM(BaseInDB):
    title: str
    desc: str
    dt: datetime
    division_int_id: Optional[int]


class ProductDBM(BaseInDB):
    title: str
    description: str
    cost: int
