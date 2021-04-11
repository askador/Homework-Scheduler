from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from bot.data import config


bot = Bot(
    token=config.test_bot_token,
    parse_mode=types.ParseMode.HTML,
)

storage = MongoStorage(uri=config.mongodb_url.replace("hw_bot_db", "aiogram_fsm"))
# storage = MongoStorage(uri="mongodb+srv://test_user:1234@cluster0.lajfk.mongodb.net/aiogram_fsm?retryWrites=true&w=majority")

dp = Dispatcher(
    bot=bot,
    storage=storage,
)


__all__ = (
    "bot",
    "storage",
    "dp",
)