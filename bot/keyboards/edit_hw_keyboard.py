from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def edit_hw_keyboard(common):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('📅  Срок сдачи', callback_data='deadline'))
    markup.add(InlineKeyboardButton('📝 Описание работы', callback_data='description'))
    if common == 'common':
        markup.add(InlineKeyboardButton('❕ Обычное', callback_data='common'))
    else:
        markup.add(InlineKeyboardButton('❗️Важное', callback_data='common'))
    markup.add(InlineKeyboardButton('➖ Удалить', callback_data='delete'))
    markup.add(InlineKeyboardButton('✖️ Завершить', callback_data='done'))
    return markup
