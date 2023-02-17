from datetime import datetime
from enum import Enum
from typing import Optional

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
    tokens: list[str]
    role: Roles
    coins: int
    position: str
    birth_date: datetime
    description: str
    telegram: str
    whatsapp: str
    vk: str
    roadmap_int_id: Optional[int]
    division_int_id: int

    def document(self) -> Document:
        doc = super().document()
        doc['role'] = self.role.value
        return doc


class QuizDBM(BaseInDB):
    question: str
    answer: Optional[str]
    correct_answer: Optional[str]


class TaskTypes(str, Enum):
    auto_test = 'auto_test'
    hr_confirmation = 'hr_confirmation'
    feedback = 'feedback'


class TaskDBM(BaseInDB):
    type: TaskTypes
    title: str
    text: str
    is_confirmed_by_hr_int_id: Optional[int]
    coins: int
    is_completed: bool
    attachments: dict[str, str]
    quizzes: list[QuizDBM]

    def document(self) -> Document:
        doc = super().document()
        doc['type'] = self.type.value
        return doc


class RoadmapDBM(BaseInDB):
    title: str
    tasks: list[TaskDBM]
    created_by_int_id: str


class MailCodeDBM(BaseInDB):
    mail: str
    code: int
