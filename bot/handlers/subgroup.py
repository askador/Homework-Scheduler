from bot.loader import dp
from aiogram.dispatcher import filters

ALIAS = [
    "подгруппа"
]

@dp.message_handler(filters.Text(startswith=ALIAS), is_chat_admin=True)
async def subgroup(message):
    return await message.reply("заходи, я создал")