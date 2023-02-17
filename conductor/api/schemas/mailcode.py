from pydantic import BaseModel


class OperationStatus(BaseModel):
    is_done: bool
