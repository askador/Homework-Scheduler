from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import filters


@dp.message_handler(filters.IsReplyFilter(is_reply=True), filters.Text(startswith="!повысить"),  access_level='creator')
async def promote(message: types.Message):

    # Todo
    # db

    await bot.send_message(message.chat.id, "Повышение!!!")