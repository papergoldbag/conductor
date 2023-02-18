from typing import Optional

from fastapi import Depends, HTTPException, Header
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


def get_strict_current_user(user: UserDBM = Depends(get_current_user)) -> UserDBM:
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='no user')
    return user


def make_strict_depends_on_roles(roles: list[str]):
    def wrapper(current_user: UserDBM = Depends(get_strict_current_user)) -> UserDBM:
        if current_user.role not in roles:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'u r not {roles}')
        return current_user

    return wrapper
