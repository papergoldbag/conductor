from conductor.core.misc import settings
from conductor_bot.consts import bot


async def send_to_admins(msg: str):
    for admin_id in settings.tg_admin_ids:
        await bot.send_message(chat_id=admin_id, text=msg.strip(), disable_web_page_preview=True)
