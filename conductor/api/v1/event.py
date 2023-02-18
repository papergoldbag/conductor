from fastapi import APIRouter, Body, Depends
from conductor.api.dependencies import make_strict_depends_on_roles
from conductor.api.schemas.event import CreateEvent
from conductor.core.misc import db
from conductor.db.models import EventDBM, Roles, UserDBM
from typing import Optional

from fastapi import APIRouter

event_router = APIRouter()


@event_router.post('', response_model=EventDBM)
async def create_event(
        user: UserDBM = Depends(make_strict_depends_on_roles(roles=[Roles.hr, Roles.supervisor])),
        event_to_create: CreateEvent = Body()
):
    event = EventDBM(**event_to_create.dict())
    inserted = EventDBM.parse_document(db.event.insert_document(event.document()))
    return inserted


@event_router.get('.get_events_by_division_int_id', response_model=list[EventDBM])
async def events_for_division(
        division_int_id: int
):
    events = db.event.pymongo_collection.find({'division_int_id': {'$in': [division_int_id]}})
    return [EventDBM.parse_document(event) for event in events]
