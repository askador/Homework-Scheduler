from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import filters


@dp.message_handler(filters.IsReplyFilter(is_reply=True), filters.Text(startswith="!понизить"),  is_chat_admin=True)
async def demote(message: types.Message):

    # Todo
    # db

    await bot.send_message(message.chat.id, "Понижение...")