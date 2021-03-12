from bot.loader import dp
from aiogram.dispatcher import filters
from aiogram import types
from datetime import datetime, timedelta

ALIAS = [
    "дз",
    "показать дз",
    "нюдсы"
]


CHAT_TYPES = [
    types.ChatType.GROUP,
    types.ChatType.SUPERGROUP
]

@dp.message_handler(filters.Text(equals=ALIAS), filters.ChatTypeFilter(CHAT_TYPES))
async def get_hw_public(message):
    date = datetime.now() + timedelta(days=7)
    return await message.reply("Нет дз, Артьомка")