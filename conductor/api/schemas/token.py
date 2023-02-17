from pydantic import BaseModel

from conductor.api.schemas.base import BaseSchema


class TokenInOut(BaseModel):
    token: str


class TokenResponse(BaseSchema):
    out: TokenInOut
