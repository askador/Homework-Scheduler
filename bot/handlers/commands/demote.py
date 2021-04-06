from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import filters


@dp.message_handler(filters.IsReplyFilter(is_reply=True), filters.Text(startswith="!понизить"),  access_level='creator')
async def demote(message: types.Message):

    # Todo
    # db

    await bot.send_message(message.chat.id, "Понижение...")