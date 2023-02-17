from fastapi import APIRouter

echo_router = APIRouter()


@echo_router.get("")
def echo():
    return {}
