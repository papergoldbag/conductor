from conductor.db.models import DivisionDBM


class DivisionResponse(DivisionDBM):
    user_int_ids: list[int]
