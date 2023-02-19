from typing import Optional

from fastapi import APIRouter, Depends, Query
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from conductor.api.dependencies import get_current_user
from conductor.api.v1.auth import generate_token
from conductor.core.misc import templates, db
from conductor.db.models import UserDBM

pages_router = APIRouter(tags=['pages'])


@pages_router.get('/')
async def index(
        r: Request,
        user=Depends(get_current_user)
):
    if user:
        return RedirectResponse('/roadmap', status_code=status.HTTP_302_FOUND)
    return RedirectResponse('/auth', status_code=status.HTTP_302_FOUND)


@pages_router.get('/auth')
async def auth(
        r: Request,
        mail: Optional[str] = Query(None),
        code: Optional[int] = Query(None),
        user=Depends(get_current_user)
):
    if user:
        return RedirectResponse('/roadmap', status_code=status.HTTP_302_FOUND)

    if mail is not None and code is not None:
        doc = db.mail_code.pymongo_collection.find_one({
            'mail': mail.strip(),
            'code': code
        })
        if doc is not None:
            user = db.user.pymongo_collection.find_one({'email': mail.strip()})
            if user is not None:
                token = generate_token()
                db.user.pymongo_collection.update_one({'int_id': user['int_id']}, {'$push': {'tokens': token}})

                response = RedirectResponse('/roadmap', status_code=status.HTTP_302_FOUND)
                response.set_cookie(key="token", value=token)

                return response

    return templates.TemplateResponse("auth.html", {'request': r})


@pages_router.get('/roadmap')
async def roadmap(r: Request, user=Depends(get_current_user)):
    if not user:
        return RedirectResponse('/auth', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("roadmap.html", {'request': r})


@pages_router.get('/profile')
async def roadmap(r: Request, user=Depends(get_current_user)):
    if not user:
        return RedirectResponse('/auth', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("profile.html", {'request': r})


@pages_router.get('/shop')
async def roadmap(r: Request, user=Depends(get_current_user)):
    if not user:
        return RedirectResponse('/shop', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("shop.html", {'request': r})


@pages_router.get('/events')
async def roadmap(r: Request, user=Depends(get_current_user)):
    if not user:
        return RedirectResponse('/events', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("events.html", {'request': r})


@pages_router.get('/network')
async def roadmap(r: Request, user=Depends(get_current_user)):
    if not user:
        return RedirectResponse('/network', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("network.html", {'request': r})


@pages_router.get('/adduser')
async def adduser(r: Request, user=Depends(get_current_user)):
    if not user:
        return RedirectResponse('/adduser', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("adduser.html", {'request': r})


@pages_router.get('/sign_out')
async def roadmap(
        r: Request,
        user: UserDBM = Depends(get_current_user)
):
    token1 = r.headers.get('token')
    token2 = r.cookies.get('token')

    if token1 is not None:
        db.user.pymongo_collection.update_one(
            {'int_id': user.int_id},
            {'$pull': {'tokens': token1}}
        )
    if token2 is not None:
        db.user.pymongo_collection.update_one(
            {'int_id': user.int_id},
            {'$pull': {'tokens': token2}}
        )

    r = RedirectResponse('/auth', status_code=status.HTTP_302_FOUND)
    r.delete_cookie('token')
    return r
