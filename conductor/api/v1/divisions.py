from fastapi import APIRouter, Depends

from conductor.api.dependencies import get_strict_current_user
from conductor.api.schemas.division import DivisionResponse
from conductor.core.misc import db
from conductor.db.models import UserDBM

division_router = APIRouter()


@division_router.get("", response_model=list[DivisionResponse])
def get_all_divisions(user: UserDBM = Depends(get_strict_current_user)):
    division_to_users = {}
    for user_doc in db.user.pymongo_collection.find():
        user = UserDBM.parse_document(user_doc)
        if user.division_int_id not in division_to_users:
            division_to_users[user.division_int_id] = []
        division_to_users[user.division_int_id].append(user.division_int_id)

    res = []
    for division_doc in db.division.pymongo_collection.find():
        user_int_ids = []
        if division_doc['int_id'] in division_to_users:
            user_int_ids = division_to_users[division_doc['int_id']]
        res.append(DivisionResponse(
            user_int_ids=user_int_ids,
            **division_doc
        ))

    return res
