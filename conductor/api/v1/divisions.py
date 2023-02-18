from fastapi import APIRouter

from conductor.core.misc import db
from conductor.db.models import DivisionDBM

division_router = APIRouter()


@division_router.get("", response_model=list[DivisionDBM])
def get_all_divisions():
    return [DivisionDBM(doc) for doc in db.division.pymongo_collection.find()]
