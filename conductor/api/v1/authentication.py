from fastapi import APIRouter

from conductor.api.schemas.common import *

router = APIRouter()


@router.get('/mail/check', response_model=CheckResponse)
async def mail_check(mail: str):
    ...


@router.get('/mail/send_code')
async def mail_send_code(mail: str):
    ...


@router.get('/mail/check_code', response_model=CheckResponse)
async def check_sended_code(code: str):
    return {'correct': code}


@router.get('/sign_in', response_model=UsersResponse)
async def auth_user(code: str = None, mail: str = None):
    ...
