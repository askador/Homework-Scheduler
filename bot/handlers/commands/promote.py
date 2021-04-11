from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import filters

from bot.types.MongoDB import Chat


@dp.message_handler(filters.IsReplyFilter(is_reply=True),
                    filters.Command(commands="повысить", prefixes='!'),
                    access_level='creator',
                    state='*')
async def promote(message: types.Message):
    new_moder = message.reply_to_message.from_user.id
    name = message.reply_to_message.from_user.full_name

    chat = Chat(message.chat.id)

    admins = await chat.get_field_value("admins")
    if new_moder in admins:
        return
    admins.append(new_moder)
    await chat.update(title=message.chat.title, admins=admins)

    await message.answer(f"<a href='tg://user?id={new_moder}'>{name}</a> новый модератор!")
