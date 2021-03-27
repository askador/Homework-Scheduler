import os

from pymongo import MongoClient
from aiogram.dispatcher import filters
from aiogram.types import InputMediaPhoto, ChatType
from datetime import datetime, timedelta
from pprint import pprint

from bot.loader import dp, bot
from bot.data import config
from bot.states.get_public_hw import ShowHw
from bot.keyboards.show_homework.show_homework import homework_kb_next_week
from bot.types.HomeworksList import HomeworksList
from bot.utils.methods.get_files_pathes import get_files_pathes

from time import sleep

ALIAS = [
    "!п",
    "!показать дз"
]


CHAT_TYPES = [
    ChatType.GROUP,
    ChatType.SUPERGROUP
]


@dp.message_handler(filters.Text(equals=ALIAS), state='*')
@dp.message_handler(filters.Command(commands=["п", "показать дз"], prefixes=["!"]), state='*')
async def get_hw_public(message, state):
    chat_id = message.chat.id

    """Reset state config"""

    async with state.proxy() as data:
        data['week_page'] = 0

    await ShowHw.week.set()
    # col.update_one({"chat": message.chat.id, "user": message.from_user.id}, {"$set": {"data": {"week_page": 0}}})

    """Generate homeworks"""
    loading = await message.reply("Загрузка...")
    # html_path, photo_path = get_files_pathes(chat_id)

    hws_list = HomeworksList(chat_id=chat_id, page=0)

    # hw_data = await hws_list.generate_photo(html_file=html_path, photo_file=photo_path)
    hw_data = await hws_list.generate_text()

    await bot.delete_message(chat_id=chat_id, message_id=loading.message_id)

    a = await message.answer(hw_data, reply_markup=homework_kb_next_week)

    # a = await message.answer_photo(hw_data, reply_markup=homework_kb_next_week)
    print(a)

    # os.remove(html_path)
    # os.remove(photo_path)





