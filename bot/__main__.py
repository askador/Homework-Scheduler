import logging

from aiogram import Dispatcher
from aiogram.utils import executor

from bot import utils
from bot.loader import dp
from bot.data import config

# The configuration of the modules using import
from bot import handlers
from bot.handlers import inline


async def on_startup(dispatcher: Dispatcher):
    pass
    # await utils.setup_default_commands(dispatcher)
    # await utils.notify_admins(config.SUPERUSER_IDS)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # utils.setup_logger("INFO", ["sqlalchemy.engine", "aiogram.bot.api"])
    executor.start_polling(
        dp, on_startup=on_startup, skip_updates=True
    )
