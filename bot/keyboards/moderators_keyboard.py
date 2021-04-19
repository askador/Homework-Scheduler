from bot.loader import bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.types.MongoDB.Collections import Chat


async def moderators_keyboard(chat_id):
    markup = InlineKeyboardMarkup()
    chat = Chat(chat_id)

    moderators = await chat.get_field_value('admins')

    for moderator in moderators:
        user = (await bot.get_chat_member(chat_id, moderator)).user
        markup.row(InlineKeyboardButton(user.full_name, callback_data=moderator),
                   InlineKeyboardButton("👤", url='https://t.me/{}'.format(user.username)))
    return markup