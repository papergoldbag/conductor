from typing import Optional

from fastapi import Security, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from conductor.core.misc import db
from conductor.db.models import UserDBM


def get_current_user(ac: HTTPAuthorizationCredentials = Security(HTTPBearer())) -> UserDBM:
    user = db.user.pymongo_collection.find_one({'tokens': {"$in": [ac, ]}})
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'asf': 'af'})
    return UserDBM.parse_document(user)


def get_current_hr(current_user: Optional[UserDBM] = Depends(get_current_user)) -> UserDBM:
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'asf': 'af'})
    return current_user
