from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .select_time import select_time_keyboard


async def settings_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('📚 Предметы', callback_data='subj_settings'))
    markup.add(InlineKeyboardButton('🚻 Подгруппы', callback_data='subgr_settings'))
    markup.add(InlineKeyboardButton('🔔 Уведомления', callback_data='notifications_settings'))
    markup.add(InlineKeyboardButton('📅 Сроки', callback_data='terms_settings'))
    markup.add(InlineKeyboardButton('🖼 Внешний вид', callback_data='style_settings'))
    markup.add(InlineKeyboardButton('✖️ Завершить', callback_data='close_settings'))
    return markup


async def settings_keyboard_subjects():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        [
            InlineKeyboardButton('➕ Добавить предметы', callback_data='add_subjs'),
            InlineKeyboardButton('➖ Убрать предметы', callback_data='remove_subjs')
        ]
    )
    markup.row_width(1)
    markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back'))
    markup.add(InlineKeyboardButton('✖️ Завершить', callback_data='done'))
    return markup


async def settings_keyboard_subgroups():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        [
            InlineKeyboardButton('➕ Добавить подгруппу', callback_data='add'),
            InlineKeyboardButton('❌ Удалить подгруппу', callback_data='remove')
        ]
    )
    markup.row_width(1)
    markup.add(InlineKeyboardButton('➖ Изменить состав', callback_data='edit'))
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