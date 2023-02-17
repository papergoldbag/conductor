import binascii
import os
from random import randint

from fastapi import APIRouter

from conductor.api.schemas.base import BaseSchema
from conductor.api.schemas.token import TokenInOut, TokenResponse
from conductor.core.misc import db
from conductor.db.models import MailCodeDBM

auth_router = APIRouter()


def generate_token() -> str:
    res = binascii.hexlify(os.urandom(20)).decode() + str(randint(10000, 1000000))
    return res[:128]


def generate_mail_code() -> str:
    return f'{randint(1, 9)}{randint(1, 9)}{randint(1, 9)}{randint(1, 9)}'


@auth_router.post('', response_model=TokenResponse)
async def auth(mail: str, code: str):
    doc = db.mail_code.pymongo_collection.find_one({
        'mail': mail,
        'code': code
    })
    return TokenResponse(out=TokenInOut(token=generate_token()))


@auth_router.get('.send_mail_code', response_model=BaseSchema)
async def send_mail_code(mail: str):
    doc = db.mail_code.insert_document(MailCodeDBM(mail=mail, code=generate_mail_code()).document())
    return BaseSchema()
