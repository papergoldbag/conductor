from pydantic import BaseModel

from conductor.db.models import TaskTypes, Attachment, QuizDBM


class CreateTaskDBM(BaseModel):
    type: TaskTypes
    title: str
    text: str
    coins: int
    week_num: int
    day_num: int
    attachments: list[Attachment]
    quizzes: list[QuizDBM]

    def dict(self, *args, **kwargs):
        doc = super().dict(*args, **kwargs)
        doc['type'] = self.type.value
        return doc


class CreateRoadmapTemplate(BaseModel):
    title: str
    tasks: list[CreateTaskDBM]
