from typing import Optional

from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from conductor.core.misc import db
from conductor.db.models import User


def get_current_user(ac: HTTPAuthorizationCredentials = Security(HTTPBearer())) -> Optional[User]:
    user = db.user.pymongo_collection.find_one({'tokens': {"$in": [ac, ]}})
    if user is None:
        return None
    return User.parse_document(user)
