import binascii
import os
from random import randint

from fastapi import APIRouter

from conductor.api.schemas.auth import TokenOutResponse, TokenOut
from conductor.api.schemas.common import *
from conductor.core.misc import db
from conductor.db.models import MailCode

router = APIRouter()


def generate_token() -> str:
    res = binascii.hexlify(os.urandom(20)).decode() + str(randint(10000, 1000000))
    return res[:128]


def generate_mail_code() -> str:
    return f'{randint(1, 9)}{randint(1, 9)}{randint(1, 9)}{randint(1, 9)}'


@router.post('', response_model=TokenOutResponse)
async def auth(mail: str, code: str):
    doc = db.mail_code.pymongo_collection.find_one({
        'mail': mail,
        'code': code
    })
    return TokenOutResponse(out=TokenOut(token=generate_token()))


@router.get('.send_mail_code', response_model=CommonResponse)
async def send_mail_code(mail: str):
    doc = db.mail_code.insert_document(MailCode(mail=mail, code=generate_mail_code()).document())
    return CommonResponse(out={'code': generate_mail_code()})


# @router.get('.check_mail_code', response_model=CheckResponse)
# async def check_sended_code(code: str):
#     return {'correct': code}
#
#
# @router.get('/', response_model=UsersResponse)
# async def auth_user(code: str = None, mail: str = None):
#     ...
