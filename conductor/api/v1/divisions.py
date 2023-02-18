from fastapi import APIRouter, Depends

from conductor.api.dependencies import get_strict_current_user
from conductor.core.misc import db
from conductor.db.models import DivisionDBM, UserDBM

division_router = APIRouter()


@division_router.get("", response_model=list[DivisionDBM])
def get_all_divisions(user: UserDBM = Depends(get_strict_current_user)):
    return [DivisionDBM(doc) for doc in db.division.pymongo_collection.find()]
