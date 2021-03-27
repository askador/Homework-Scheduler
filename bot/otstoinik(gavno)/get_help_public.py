from bot.loader import dp
from aiogram.dispatcher import filters
from aiogram import types

ALIAS = [
    "справка",
    "хелп"
]

COMMANDS = [
    "help",
    "info"
]

CHAT_TYPES = [
    types.ChatType.GROUP,
    types.ChatType.SUPERGROUP
]


@dp.message_handler(commands=COMMANDS,  is_chat_admin=True)
@dp.message_handler(filters.Text(startswith=ALIAS),  is_chat_admin=True)
async def get_help_public(message):
    return await message.reply("Список комманд:\n"
        "добавить дз  -  добавить его если вы администратор\n"
        "показать дз - домашка\n"
        ,reply = False)