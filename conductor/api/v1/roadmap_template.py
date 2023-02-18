from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from conductor.api.dependencies import get_strict_current_user
from conductor.api.schemas.roadmap import RoadmapResponse
from conductor.core.misc import db
from conductor.db.models import RoadmapDBM, UserDBM

roadmap_template_router = APIRouter()


@roadmap_template_router.post('.create')
async def create_roadmap_template():
    pass
