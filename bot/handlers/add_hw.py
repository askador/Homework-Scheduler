from bot.loader import dp
from aiogram.dispatcher import filters
#from datetime import datetime, timedelta

ALIAS = [
    "добавить дз"
]

@dp.message_handler(filters.Text(equals=ALIAS), is_chat_admin=True)
async def add_hw(message):
    return await message.reply("Не надо мне еще дз")