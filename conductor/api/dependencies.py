from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from conductor.db.models import User


# def get_current_user(ac: HTTPAuthorizationCredentials = Security(HTTPBearer())) -> User:
#     user = db.user_by_token(s, token=ac.credentials)
#     if not user:
#         raise HTTPException(status.HTTP_403_FORBIDDEN, "Not authenticated")
#     return