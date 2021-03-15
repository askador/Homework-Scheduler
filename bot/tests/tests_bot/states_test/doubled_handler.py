import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.mongo import MongoStorage


from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from bot.data import config

bot = Bot(
    token=config.token,
    parse_mode=types.ParseMode.HTML,
)

dp = Dispatcher(
    bot=bot,
)


@dp.message_handler()
async def first_layer(mes):
    await mes.reply(not mes.text.isdigit())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # utils.setup_logger("INFO", ["sqlalchemy.engine", "aiogram.bot.api"])
    executor.start_polling(
        dp, skip_updates=True
    )
