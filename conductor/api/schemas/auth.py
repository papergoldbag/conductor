from pydantic import BaseModel

from conductor.api.schemas.common import CommonResponse


class TokenOut(BaseModel):
    token: str


class TokenOutResponse(CommonResponse):
    out: TokenOut
