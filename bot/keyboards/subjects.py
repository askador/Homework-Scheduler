from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

subj = [
    "ООП",
    "ОП",
    "Мат",
    "Анал"
]


async def subjects_keyboard(subjects, page):

    async def asrange(a, b):
        for i in range(a, b):
            yield (i)

    markup = InlineKeyboardMarkup()

    if len(subjects) <= 7:
        async for sub in asrange(0, len(subjects)):
            markup.add(InlineKeyboardButton(subjects[sub], callback_data=subjects[sub]))
    elif page == 1:
        async for sub in asrange(0, 6):
            markup.add(InlineKeyboardButton(subjects[sub], callback_data=subjects[sub]))
            print(sub)
        markup.add(InlineKeyboardButton('Следующая страница', callback_data='next'))
    elif len(subjects) <= 12+(5*(page-2)):
        async for sub in asrange((5*(page-2)+6), len(subjects)):
            markup.add(InlineKeyboardButton(subjects[sub], callback_data=subjects[sub]))
            print(sub)
        markup.add(InlineKeyboardButton('Предыдущая страница', callback_data='back'))
    else:
        async for sub in asrange((5*(page-2)+6), (5*(page-1)+6)):
            markup.add(InlineKeyboardButton(subjects[sub], callback_data=subjects[sub]))
            print(sub)
        markup.add(InlineKeyboardButton('Предыдущая страница', callback_data='back'))
        markup.add(InlineKeyboardButton('Следующая страница', callback_data='next'))
    return markup
