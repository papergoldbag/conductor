from pydantic import BaseModel

from conductor.db.models import RoadmapDBM


class RoadmapResponse(RoadmapDBM):
    weeks: list[int]
    days: list[int]
    week_to_days: dict[int, list[int]]
