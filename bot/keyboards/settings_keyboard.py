from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def settings_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Предметы', callback_data='0'))
    markup.add(InlineKeyboardButton('Подгруппы', callback_data='1'))
    markup.add(InlineKeyboardButton('Уведомления', callback_data='2'))
    markup.add(InlineKeyboardButton('Сроки', callback_data='3'))
    return markup