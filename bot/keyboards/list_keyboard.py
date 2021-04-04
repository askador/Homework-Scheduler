from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.types.MongoDB.Collections import Chat
from bot.utils.methods.generate_hws_kb import generate_hws_kb


async def list_keyboard(chat_id, filter, page):

    async def asrange(a, b):
        for i in range(a, b):
            yield (i)

    list_height = 3

    chat = Chat(chat_id)

    array = []
    if filter == 'subject':
        array = await chat.get_field_value("subjects")
    elif filter == 'subgroup':
        array.append("Все")
        array += await chat.get_field_value("subgroups")
    elif filter == 'homeworks':
        homeworks = await chat.get_homeworks(filters=[{}], full_info=False)

        index = 1

        for hw in homeworks:
            hw = hw['_id']
            button_text = f"{index}. {hw['subject']} "

            if hw['subgroup'] != '':
                button_text += f"{hw['subgroup']}пг. "

            button_text += f"{hw['name']}"

            array.append(button_text)

            index += 1

    markup = InlineKeyboardMarkup()

    if len(array) <= list_height:
        async for elem in asrange(0, len(array)):
            markup.add(InlineKeyboardButton(array[elem], callback_data=array[elem]))
    elif page == 1:
        async for elem in asrange(0, (list_height-1)):
            markup.add(InlineKeyboardButton(array[elem], callback_data=array[elem]))
        markup.add(InlineKeyboardButton('Следующая страница', callback_data='next'))
    elif len(array) <= (2*(list_height-1)) + ((list_height-2) * (page - 2)):
        async for elem in asrange(((list_height-2) * (page - 2) + (list_height-1)), len(array)):
            markup.add(InlineKeyboardButton(array[elem], callback_data=array[elem]))
        markup.add(InlineKeyboardButton('Предыдущая страница', callback_data='back'))
    else:
        async for elem in asrange(((list_height-2)*(page-2)+(list_height-1)), ((list_height-2)*(page-1)+(list_height-1))):
            markup.add(InlineKeyboardButton(array[elem], callback_data=array[elem]))
        markup.add(InlineKeyboardButton('⬅️ Предыдущая страница', callback_data='back'))
        markup.add(InlineKeyboardButton('Следующая страница  ➡️', callback_data='next'))

    return markup
