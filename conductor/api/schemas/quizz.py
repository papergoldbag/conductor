from pydantic import BaseModel
class SendAnswers(BaseModel):
    task_num: int
    answers: list[str]
