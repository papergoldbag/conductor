from typing import Optional

from fastapi import Security, Depends, HTTPException, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status
from starlette.requests import Request

from conductor.core.misc import db
from conductor.db.models import UserDBM


def get_current_user(*, token: str = Header(None), req: Request) -> Optional[UserDBM]:
    token_cookie: str = req.cookies.get('token')
    if not token and not token_cookie:
        return None

    token = token if token else token_cookie

    user = db.user.pymongo_collection.find_one({'tokens': {"$in": [token]}})
    if user is None:
        return None
    return UserDBM.parse_document(user)


def make_depends_on_role(role: str):
    def wrapper(current_user: Optional[UserDBM] = Depends(get_current_user)) -> UserDBM:
        if current_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='no user')
        if current_user.role != role:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'u r not {role}')
        return current_user

    return wrapper
