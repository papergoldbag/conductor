from typing import Optional

from fastapi import Security, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from conductor.core.misc import db
from conductor.db.models import UserDBM, Roles


def get_current_user(ac: HTTPAuthorizationCredentials = Security(HTTPBearer())) -> UserDBM:
    user = db.user.pymongo_collection.find_one({'tokens': {"$in": [ac.credentials]}})
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='bad token')
    return UserDBM.parse_document(user)


def get_current_hr(current_user: Optional[UserDBM] = Depends(get_current_user)) -> UserDBM:
    if current_user.role != Roles.hr:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='u r not hr')
    return current_user


def get_current_employee(current_user: Optional[UserDBM] = Depends(get_current_user)) -> UserDBM:
    if current_user.role != Roles.employee:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='u r not employee')
    return current_user


def get_current_supervisor(current_user: Optional[UserDBM] = Depends(get_current_user)) -> UserDBM:
    if current_user.role != Roles.supervisor:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='u r not supervisor')
    return current_user
