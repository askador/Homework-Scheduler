from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.data import config


bot = Bot(
    token="1173133322:AAG_E7H2IjRypO3dt-pygUjh9V1HP8X8JPk",
    parse_mode=types.ParseMode.HTML,
)

storage = MemoryStorage()

dp = Dispatcher(
    bot=bot,
    storage=storage,
)
