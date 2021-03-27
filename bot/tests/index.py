from aiogram import Bot,Dispatcher, executor
from bot.data import config
import logging

from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle

logging.basicConfig(level=logging.INFO)
bot = Bot(token = config.token)
dp = Dispatcher(bot)


# from aiogram import filters
# from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle


# @dp.inline_handler()
# async def test_inline(inline):
#         print(inline)


# async def on_startup(dp):
#     from bot.utils import set_commands
#     await set_commands(dp)
#

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

