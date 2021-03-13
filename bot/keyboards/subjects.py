from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

subj = [
    "ООП",
    "ОП",
    "Мат",
    "Анал"
]

async def subjects_keyboard(subjects):

    async def asrange(count):
        for i in range(count):
            yield (i)

    if(len(subjects) <= 7):
        markup = InlineKeyboardMarkup()
        async for sub in asrange(len(subjects)):
            markup.add(InlineKeyboardButton(subjects[sub], callback_data = '{}'.format(sub)))
        return markup
    else:
        markup = InlineKeyboardMarkup()
        for sub in asrange(6):
            markup.add(InlineKeyboardButton(subjects[sub], callback_data = '{}'.format(sub)))
            print(sub)
        markup.add(InlineKeyboardButton('Следующая страница', callback_data='next'))
        return markup
