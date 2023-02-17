from pydantic import BaseModel, EmailStr


class AuthSchema(BaseModel):
    mail: EmailStr
    code: int
