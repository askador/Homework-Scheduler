from aiogram import Bot,Dispatcher, executor
from bot.data import config
import logging

logging.basicConfig(level=logging.INFO)
bot = Bot(token = config.token)
dp = Dispatcher(bot)

#
# @dp.message_handler()
# async def mes(msg):
#

from aiogram import filters
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle






# async def on_startup(dp):
#     from bot.utils import set_commands
#     await set_commands(dp)
#

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

