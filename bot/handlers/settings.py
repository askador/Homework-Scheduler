from bot.loader import dp
from aiogram.dispatcher import filters
from aiogram import types
from bot.keyboards import settings_keyboard

ALIAS = [
    "настройки"
]


CHAT_TYPES = [
    types.ChatType.GROUP,
    types.ChatType.SUPERGROUP
]


@dp.message_handler(filters.Text(equals=ALIAS), filters.ChatTypeFilter(CHAT_TYPES))
async def settings(message):
    markup = await settings_keyboard()
    return await message.reply("Себя настрой лучше", reply_markup=markup)
