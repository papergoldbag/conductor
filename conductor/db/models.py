from datetime import date
from enum import Enum
from typing import Optional

from conductor.db.base import BaseInDB, Document


class Division(BaseInDB):
    title: str


class User(BaseInDB):
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


class Quiz(BaseInDB):
    question: str
    answer: str
    correct_answer: str


class TaskTypes(str, Enum):
    auto_test = 'auto_test'
    ht_confirmation = 'ht_confirmation'
    feedback = 'feedback'


class Task(BaseInDB):
    type: TaskTypes
    title: str
    text: str
    attachments: dict[str, str]
    quizzes: list[Quiz]
    is_confirmed_by_hr_int_id: Optional[int]
    coins: int
    is_completed: bool

    def document(self) -> Document:
        doc = super().document()
        doc['type'] = self.type.value
        return doc


class Roadmap(BaseInDB):
    title: str
    tasks: dict[int, Task]
    created_by_int_id: str
