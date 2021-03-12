from bot.loader import dp
from aiogram.dispatcher import filters
from aiogram import types

ALIAS = [
    "справка",
    "хелп"
]

CHAT_TYPES = [
    types.ChatType.GROUP,
    types.ChatType.SUPERGROUP
]

@dp.message_handler(filters.Text(equals=ALIAS), filters.ChatTypeFilter(CHAT_TYPES))
async def get_help_public(message):
    return await message.reply("Список комманд:\n"
        "добавить дз  -  добавить его если вы администратор\n"
        "показать дз - домашка\n"
        ,reply = False)