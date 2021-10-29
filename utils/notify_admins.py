from loguru import logger
from aiogram import Dispatcher
from aiogram.types import ParseMode

from config import TELEGRAM_ADMINS


async def notify_admins(dispatcher: Dispatcher, message: str, header='NOTIFY SYSTEM'):
    notify = '\n'.join([
        f"<code>{header}</code>",
        f"<b>{message}</b>",
    ])

    for admin_id in TELEGRAM_ADMINS:
        try:
            await dispatcher.bot.send_message(admin_id, notify, parse_mode=ParseMode.HTML)
        except Exception as err:
            logger.exception(err)