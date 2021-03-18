from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def settings_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Предметы', callback_data='0'))
    markup.add(InlineKeyboardButton('Подгруппы', callback_data='1'))
    markup.add(InlineKeyboardButton('Уведомления', callback_data='2'))
    markup.add(InlineKeyboardButton('Сроки', callback_data='3'))
    markup.add(InlineKeyboardButton('Завершить', callback_data='4'))
    return markup


async def settings_keyboard_subjects():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Добавить предметы', callback_data='add'))
    markup.add(InlineKeyboardButton('Убрать предметы', callback_data='remove'))
    markup.add(InlineKeyboardButton('Завершить', callback_data='done'))
    return markup


async def settings_keyboard_subgroups():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Изменить состав', callback_data='add'))
    markup.add(InlineKeyboardButton('Удалить подгруппу', callback_data='remove'))
    markup.add(InlineKeyboardButton('Завершить', callback_data='done'))
    return markup


async def settings_keyboard_notifications():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Завершить', callback_data='done'))
    return markup


async def settings_keyboard_terms():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Завершить', callback_data='done'))
    return markup
