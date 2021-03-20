import logging
import os
from datetime import datetime, timedelta

from aiogram.types import ContentType
from pymongo import MongoClient
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text, Command
from bot.loader import bot, dp
from bot.data import config
# from generate_png import generate_png
from bot.types.HomeworksList import HomeworksList
from bot.handlers import get_hw_public
from bot.handlers.callback_query import next_week, prev_week


@dp.message_handler(Text(equals="пок1231азать дз"), state='*')
async def show_png(msg):
    pass


@dp.message_handler(content_types=ContentType.PHOTO)
async def get_photo_id(msg):
    for x in msg.photo:
        print(x)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(
        dp, skip_updates=True
    )
