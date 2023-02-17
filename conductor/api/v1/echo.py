from fastapi import APIRouter

from conductor.api.dependencies import get_current_hr

echo_router = APIRouter()


@echo_router.get("")
def echo():
    return {}
