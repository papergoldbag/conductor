from fastapi import APIRouter

from conductor.api.schemas.common import *

router = APIRouter()


@router.post('', response_model=CheckResponse)
async def auth(mail: str):
    ...


@router.get('.send_mail_code')
async def send_mail_code(mail: str):
    ...


# @router.get('.check_mail_code', response_model=CheckResponse)
# async def check_sended_code(code: str):
#     return {'correct': code}
#
#
# @router.get('/', response_model=UsersResponse)
# async def auth_user(code: str = None, mail: str = None):
#     ...
