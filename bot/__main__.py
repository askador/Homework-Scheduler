import logging

from aiogram import Dispatcher
from aiogram.utils import executor
from bot.loader import dp

from bot import filters
from bot import handlers


async def on_startup(dp: Dispatcher):
    from bot.utils import set_commands
    await set_commands(dp)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(
        dp, on_startup=on_startup, skip_updates=True
    )
