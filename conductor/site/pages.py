from fastapi import APIRouter, Depends
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from conductor.api.dependencies import get_current_user
from conductor.core.misc import templates

pages_router = APIRouter(tags=['pages'])


@pages_router.get('/auth')
async def auth(r: Request, user=Depends(get_current_user)):
    if user:
        return RedirectResponse('/roadmap', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("auth.html", {'request': r})


@pages_router.get('/roadmap')
async def roadmap(r: Request, user=Depends(get_current_user)):
    if not user:
        return RedirectResponse('/auth', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("roadmap.html", {'request': r})


@pages_router.get('/sign_out')
async def roadmap(r: Request, user=Depends(get_current_user)):
    r = RedirectResponse('/auth', status_code=status.HTTP_302_FOUND)
    r.delete_cookie('token')
    return r
