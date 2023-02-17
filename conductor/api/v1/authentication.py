from fastapi import APIRouter

from conductor.api.schemas.common import *
from conductor.core.misc import db
from conductor.db.models import MailCode

router = APIRouter()


@router.post('', response_model=CheckResponse)
async def auth(mail: str):
    ...


@router.get('.send_mail_code')
async def send_mail_code(mail: str):
    pass


# @router.get('.check_mail_code', response_model=CheckResponse)
# async def check_sended_code(code: str):
#     return {'correct': code}
#
#
# @router.get('/', response_model=UsersResponse)
# async def auth_user(code: str = None, mail: str = None):
#     ...
