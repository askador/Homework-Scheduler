import logging

from aiogram import Dispatcher
from aiogram.utils import executor
from bot.loader import dp

from bot.handlers import commands, callback_query


async def on_startup(dp: Dispatcher):
    from bot.utils import set_commands
    await set_commands(dp)
    # await utils.setup_default_commands(dispatcher)
    # await utils.notify_admins(config.SUPERUSER_IDS)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(
        dp, on_startup=on_startup, skip_updates=True
    )
