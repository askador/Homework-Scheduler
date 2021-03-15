from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

subj = [
    "ООП",
    "ОП",
    "Мат",
    "Анал"
]


async def subjects_keyboard(subjects, page):

    async def asrange(count):
        for i in range(count):
            yield (i)

    markup = InlineKeyboardMarkup()

    if len(subjects) <= 7:
        async for sub in asrange(len(subjects)):
            markup.add(InlineKeyboardButton(subjects[sub], callback_data=subjects[sub]))
    elif page == 1:
        for sub in asrange(6):
            markup.add(InlineKeyboardButton(subjects[sub], callback_data=subjects[sub]))
            print(sub)
        markup.add(InlineKeyboardButton('Следующая страница', callback_data='next'))
    else:
        for sub in asrange(5):
            markup.add(InlineKeyboardButton(subjects[sub], callback_data=subjects[sub]))
            print(sub)
        markup.add(InlineKeyboardButton('Предыдущая страница', callback_data='back'))
        markup.add(InlineKeyboardButton('Следующая страница', callback_data='next'))
    return markup
