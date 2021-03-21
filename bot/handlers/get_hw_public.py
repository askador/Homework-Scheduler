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
async def get_hw_public(message, state):
    chat_id = message.chat.id

    """Reset state config"""
    client = MongoClient(config.mongodb_url)
    db = client["aiogram_fsm"]
    col = db["aiogram_state"]

    col.delete_one({"chat": message.chat.id, "user": message.from_user.id})

    col = db['aiogram_data']
    async with state.proxy() as data:
        data['week_page'] = 0
    col.delete_one({"chat": message.chat.id, "user": message.from_user.id})
    await ShowHw.week.set()
    # col.update_one({"chat": message.chat.id, "user": message.from_user.id}, {"$set": {"data": {"week_page": 0}}})

    """Generate photo"""
    loading = await message.reply("Загрузка...")
    html_path, photo_path = get_files_pathes(chat_id)

    hws_list = HomeworksList(chat_id=chat_id, page=0)
    await hws_list.set_fields()

    hw_photo = await hws_list.generate_photo(html_file=html_path, photo_file=photo_path)

    await bot.delete_message(chat_id=chat_id, message_id=loading.message_id)

    await message.answer_photo(hw_photo, reply_markup=homework_kb_next_week)

    os.remove(html_path)
    os.remove(photo_path)





