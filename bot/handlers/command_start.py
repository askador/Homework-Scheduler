from bot.loader import dp
from aiogram import types
from aiogram.dispatcher import filters

CHAT_TYPES = [
    types.ChatType.GROUP,
    types.ChatType.SUPERGROUP
]

@dp.message_handler(filters.ChatTypeFilter(CHAT_TYPES), commands=['start'], is_chat_admin=True)
async def start(message):
    return await message.reply("Привет, я Homework Scheduler! Сейчас начнется моя настройка!")