from bot.loader import dp
from aiogram.dispatcher import filters


@dp.message_handler(filters.Text(equals="chat id"), state='*')
async def get_chat_id(msg):
    await msg.reply(msg.chat.id)
