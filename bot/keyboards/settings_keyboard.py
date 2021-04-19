from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .select_time import select_time_keyboard


async def settings_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('📚 Предметы', callback_data='subject'))
    markup.add(InlineKeyboardButton('🚻 Подгруппы', callback_data='subgroup'))
    markup.add(InlineKeyboardButton('🔔 Уведомления', callback_data='notifications'))
    markup.add(InlineKeyboardButton('📅 Сроки', callback_data='terms'))
    # markup.add(InlineKeyboardButton('🔑 Модераторы', callback_data='moderators'))
    markup.add(InlineKeyboardButton('🖼 Внешний вид', callback_data='appearance'))
    markup.add(InlineKeyboardButton('✖️ Завершить', callback_data='done'))
    return markup


async def settings_keyboard_subjects():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton('➕ Добавить предметы', callback_data='add'),
        InlineKeyboardButton('➖ Убрать предметы', callback_data='remove')
    )
    markup.row_width = 1
    markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back'))
    markup.add(InlineKeyboardButton('✖️ Завершить', callback_data='done'))
    return markup


async def settings_keyboard_subgroups():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton('➕ Добавить подгруппу', callback_data='add'),
        InlineKeyboardButton('❌ Удалить подгруппу', callback_data='remove')
    )
    markup.row_width = 1
    markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back'))
    markup.add(InlineKeyboardButton('✖️ Завершить', callback_data='done'))
    return markup


async def settings_keyboard_notifications(pin, notify):
    markup = InlineKeyboardMarkup()
    if pin:
        markup.add(InlineKeyboardButton('📌 Закреплять напоминание', callback_data='pin'))
    else:
        markup.add(InlineKeyboardButton('Не закреплять напоминания', callback_data='pin'))
    if notify:
        markup.add(InlineKeyboardButton('🔔 Уведомлять о сроках сдачи', callback_data='notify'))
    else:
        markup.add(InlineKeyboardButton('🔕 Не уведомлять о сроках сдачи', callback_data='notify'))
    markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back'))
    markup.add(InlineKeyboardButton('✖️ Завершить', callback_data='done'))
    return markup


async def settings_keyboard_terms(selected):
    markup = await select_time_keyboard(selected)
    markup.row_width = 1
    markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back'))
    markup.add(InlineKeyboardButton('✖️ Завершить', callback_data='done'))
    return markup


async def settings_keyboard_moderators():
    markup = InlineKeyboardMarkup()
    # markup.add(InlineKeyboardButton('➕ Добавить модераторов', callback_data='add'))
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
        markup.add(InlineKeyboardButton('🤪 Забавный вид', callback_data='emoji'))
    else:
        markup.add(InlineKeyboardButton('🧑‍✈️Строгий вид', callback_data='emoji'))
    markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back'))
    markup.add(InlineKeyboardButton('✖️ Завершить', callback_data='done'))
    return markup