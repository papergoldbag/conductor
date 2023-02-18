from conductor.db.models import RoadmapDBM, TaskDBM


class RoadmapResponse(RoadmapDBM):
    weeks: list[int]
    days: list[int]
    week_to_days: dict[int, list[int]]
    easy_view: dict[int, dict[int, list[TaskDBM]]]
    easy_view2: dict
