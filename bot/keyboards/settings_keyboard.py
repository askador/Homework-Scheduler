from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .select_time import select_time_keyboard


async def settings_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('📚 Предметы', callback_data='0'))
    markup.add(InlineKeyboardButton('🚻 Подгруппы', callback_data='1'))
    markup.add(InlineKeyboardButton('🔔 Уведомления', callback_data='2'))
    markup.add(InlineKeyboardButton('📅 Сроки', callback_data='3'))
    markup.add(InlineKeyboardButton('🔑 Модераторы', callback_data='4'))
    markup.add(InlineKeyboardButton('🖼 Внешний вид', callback_data='5'))
    markup.add(InlineKeyboardButton('✖️ Завершить', callback_data='6'))
    return markup


async def settings_keyboard_subjects():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('➕ Добавить предметы', callback_data='add'))
    markup.add(InlineKeyboardButton('➖ Убрать предметы', callback_data='remove'))
    markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back'))
    markup.add(InlineKeyboardButton('✖️ Завершить', callback_data='done'))
    return markup


async def settings_keyboard_subgroups():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('➕ Добавить подгруппу', callback_data='add'))
    markup.add(InlineKeyboardButton('➖ Изменить состав', callback_data='edit'))
    markup.add(InlineKeyboardButton('❌ Удалить подгруппу', callback_data='remove'))
    markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back'))
    markup.add(InlineKeyboardButton('✖️ Завершить', callback_data='done'))
    return markup


async def settings_keyboard_notifications(pin):
    markup = InlineKeyboardMarkup()
    if pin:
        markup.add(InlineKeyboardButton('📌 Бот закрепляет новое дз', callback_data='pin'))
    else:
        markup.add(InlineKeyboardButton('Бот не закрепляет новое дз', callback_data='pin'))
    markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back'))
    markup.add(InlineKeyboardButton('✖️ Завершить', callback_data='done'))
    return markup


async def settings_keyboard_terms(selected):
    markup = await select_time_keyboard(selected)
    # markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back'))
    # markup.add(InlineKeyboardButton('✖️ Завершить', callback_data='done'))
    return markup


async def settings_keyboard_moderators():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('➕ Добавить модераторов', callback_data='add'))
    markup.add(InlineKeyboardButton('➖ Удалить модераторов', callback_data='remove'))
    markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back'))
    markup.add(InlineKeyboardButton('✖️ Завершить', callback_data='done'))
    return markup


async def settings_keyboard_appearance(photo, emoji):
    markup = InlineKeyboardMarkup()
    if photo:
        markup.add(InlineKeyboardButton('📷 Фото-дз', callback_data='photo'))
    else:
        markup.add(InlineKeyboardButton('📝 Дз текстом', callback_data='photo'))
    if emoji:
        markup.add(InlineKeyboardButton('🧑‍✈️Строгий вид', callback_data='emoji'))
    else:
        markup.add(InlineKeyboardButton('🤪 Забавный вид', callback_data='emoji'))
    markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back'))
    markup.add(InlineKeyboardButton('✖️ Завершить', callback_data='done'))
    return markup