from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def edit_hw_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Срок сдачи', callback_data='deadline'))
    markup.add(InlineKeyboardButton('Описание работы', callback_data='description'))
    markup.add(InlineKeyboardButton('Удалить', callback_data='delete'))
    markup.add(InlineKeyboardButton('Завершить', callback_data='done'))
    return markup
