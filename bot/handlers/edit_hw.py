from bot.loader import dp
from aiogram.dispatcher import filters

ALIAS = [
    "изменить дз",
    "обновить дз"
]

@dp.message_handler(filters.Text(startswith=ALIAS), is_chat_admin=True)
async def edit_hw(message):
    return await message.reply("ты че резкий")