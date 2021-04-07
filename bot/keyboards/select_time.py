from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def select_time_keyboard(selected):
    markup = InlineKeyboardMarkup()

    for r in range(4):
        markup.row()
        for c in range(6):
            id = 6*r + c
            if id != selected:
                text = str(id)+":00"
            else:
                text = "✅" + str(id)+":00"
            markup.insert(InlineKeyboardButton(text, callback_data=str(id)))

    return markup
