import logging
import os
from datetime import datetime, timedelta
from pprint import pprint

from aiogram.types import ContentType
from pymongo import MongoClient
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text, Command
from bot.loader import bot, dp
from bot.data import misc, config
# from bot.handlers.get_hw_public import get_hw_public
# from bot.handlers.callback_query import next_week, prev_week
from bot.handlers.commands import command_help


@dp.message_handler(Text(equals="чек"), user_id=526497876, state='*')
async def add_chat(msg):
    client = MongoClient(config.mongodb_url)
    db = client['hw_bot_db']
    col = db['chat']
    #
    # col.update_one({"_id": -1001424619068}, {"$push": {"homeworks":
    #     {
    #         '_id': 11,
    #         'subject': 'чм',
    #         'subgroup': '',
    #         'name': 'лаба',
    #         'description': 'описание описание описание описание описание описание описание',
    #         'deadline': datetime(2021, 3, 15, 0, 0),
    #         'priority': 0
    #     },
    # }})


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(
        dp, skip_updates=True
    )
