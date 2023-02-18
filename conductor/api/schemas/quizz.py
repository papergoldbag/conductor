from pydantic import BaseModel
class SendQuizz(BaseModel):
    task_num: int
    answers: list[str]
