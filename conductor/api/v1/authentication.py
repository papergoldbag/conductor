from fastapi import APIRouter

router = APIRouter()


@router.get('/mail/check')
async def mail_check(mail: str):
    return {'mail': mail}


@router.get('/mail/send_code')
async def mail_send_code(mail: str):
    return {'code sent to mail': mail}


@router.get('/mail/check_code')
async def check_sended_code(code: str):
    return {'code': code}


@router.get('/sign_in')
async def auth_user(code: str = None, mail: str = None):
    return {'code': code, 'mail': mail}
