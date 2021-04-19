from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import filters

from bot.types.MongoDB import Chat
from bot.utils.methods import bind_student_to_chat


@dp.message_handler(filters.IsReplyFilter(is_reply=True),
                    filters.Command(commands="понизить", prefixes='!'),
                    access_level='creator',
                    state='*')
async def demote(message: types.Message):
    await bind_student_to_chat(message.from_user.id, message.chat.id)

    moder = message.reply_to_message.from_user.id
    name = message.reply_to_message.from_user.full_name

    chat = Chat(message.chat.id)

    admins = await chat.get_field_value("admins")
    if moder not in admins:
        return

    del admins[admins.index(moder)]
    await chat.update(title=message.chat.title, admins=admins)

    await message.answer(f"<a href='tg://user?id={moder}'>{name}</a> больше не модератор")
