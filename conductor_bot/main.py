import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from aiogram.utils.executor import Executor

from conductor.core.misc import settings
from conductor.core.setup_logging import setup_logging
from conductor_bot.handlers.user import register_user_handlers

logger = logging.getLogger(__name__)


def register_all_filters(dp):
    ...


def register_all_handlers(dp):
    register_user_handlers(dp)


def main():
    setup_logging()

    bot = Bot(token=settings.tg_bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(bot, storage=MemoryStorage())
    executor = Executor(dispatcher=dp, skip_updates=True)

    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    executor.start_polling(reset_webhook=True, fast=True)


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
