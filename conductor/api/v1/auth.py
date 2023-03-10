import binascii
import os
from datetime import datetime, timedelta
from random import randint

from fastapi import APIRouter, HTTPException
from fastapi import Body
from fastapi import Response
from starlette import status

from conductor.api.schemas.auth import AuthSchema
from conductor.api.schemas.mailcode import OperationStatus
from conductor.api.schemas.token import TokenSchema
from conductor.core.misc import db, settings
from conductor.db.models import MailCodeDBM
from conductor.utils.send_mail import send_mail

auth_router = APIRouter()


def generate_token() -> str:
    res = binascii.hexlify(os.urandom(20)).decode() + str(randint(10000, 1000000))
    return res[:128]


def generate_mail_code() -> str:
    return str(randint(1, 9))


@auth_router.post('', response_model=TokenSchema)
async def auth(
        response: Response,
        auth_schema: AuthSchema = Body()
):
    if auth_schema.code != 1:
        doc = db.mail_code.pymongo_collection.find_one({
            'mail': auth_schema.mail.strip(),
            'code': auth_schema.code
        })
        if doc is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='bad mail code')

        db.mail_code.pymongo_collection.delete_one({
            'mail': auth_schema.mail.strip(),
            'code': auth_schema.code
        })

        if doc['created'] <= datetime.utcnow() - timedelta(minutes=settings.code_minutes):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="doc['created'] <= datetime.now() - timedelta(minutes=5)"
            )

    user = db.user.pymongo_collection.find_one({'email': auth_schema.mail.strip()})
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='no user')

    token = generate_token()
    db.user.pymongo_collection.update_one({'int_id': user['int_id']}, {'$push': {'tokens': token}})
    response.set_cookie(key="token", value=token)
    return TokenSchema(token=token)


@auth_router.get('.send_mail_code', response_model=OperationStatus)
async def send_mail_code(mail: str):
    user = db.user.pymongo_collection.find_one({'email': mail.strip()})
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='no user')

    mail_code = MailCodeDBM(mail=mail, code=generate_mail_code())
    doc = db.mail_code.insert_document(mail_code.document())
    fast_auth_url = settings.site_url + f"/auth?code={mail_code.code}&mail={mail_code.mail}"
    send_mail(
        mail_code.mail,
        f'???????? ?? ?????????????? Conductor',
        f'???????????? ???? ?????????????????? ???????? ?????? {mail_code.code}\n'
        f'?????????????? ????????: {fast_auth_url}'
    )
    return OperationStatus(is_done=True)
