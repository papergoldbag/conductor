from fastapi import APIRouter
from conductor.api.dependencies import get_strict_current_user
from conductor.core.misc import db
from conductor.db.models import EventDBM, UserDBM
from typing import Optional

from fastapi import APIRouter, Depends, Query
from fastapi import HTTPException, Body
from starlette import status

event_router = APIRouter()


@event_router.get('.events_for_user', response_model=list[EventDBM])
async def get_events_for_user(
    user_int_id: int
):
    events = db.event.pymongo_collection.find({'to_user_int_ids': {'$in': [user_int_id]}})
    return [EventDBM.parse_document(event) for event in events]


@event_router.get('.events_for_division', response_model=list[EventDBM])
async def events_for_division(
    division_int_id: int
):
    events = db.event.pymongo_collection.find({'division_int_id': {'$in': [division_int_id]}})
    return [EventDBM.parse_document(event) for event in events]

