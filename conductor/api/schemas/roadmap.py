from pydantic import BaseModel

from conductor.api.schemas.base import BaseSchema
from conductor.db.models import RoadmapDBM


class RoadmapInOut(BaseModel):
    roadmap: RoadmapDBM


class RoadmapResponse(BaseSchema):
    out: RoadmapInOut
