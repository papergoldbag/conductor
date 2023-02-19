import logging

from conductor.core.misc import settings
from conductor_bot.consts import bot


log = logging.getLogger(__name__)


async def send_to_admins(msg: str):
    for admin_id in settings.tg_admin_ids:
        try:
            await bot.send_message(chat_id=admin_id, text=msg.strip(), disable_web_page_preview=True)
        except Exception as e:
            log.error(e)
