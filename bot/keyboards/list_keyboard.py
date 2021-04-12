from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.types.MongoDB.Collections import Chat


async def list_keyboard(chat_id, filters, page, arr=None):
    """

    :param int chat_id: chat id
    :param str filters:
    :param str filters: either subject or subgroup or homeworks
    :param int page: keyboard page
    :param list arr: array
    """

    async def asrange(a, b):
        for i in range(a, b):
            yield i

    list_height = 7

    chat = Chat(chat_id)

    array = []
    data = []
    if filters == 'subject':
        array = await chat.get_field_value("subjects")
        data = array
    elif filters == 'subgroup':
        array.append("Все")
        data.append("any")
        array += await chat.get_field_value("subgroups")
        data += await chat.get_field_value("subgroups")
    elif filters == 'homework':
        homeworks = arr

        index = 1

        for hw in homeworks:
            hw = hw['_id']
            button_text = f"{index}. {hw['subject']} "

            if hw['subgroup'] != 'any':
                button_text += f"{hw['subgroup']}пг. "

            button_text += f"{hw['name']}"

            array.append(button_text)
            data.append('{}'.format(hw['_id']))

            index += 1
    elif filters == 'special':
        array = arr
        data = [i for i in range(0, len(arr))]

    markup = InlineKeyboardMarkup()

    if len(array) <= list_height:
        async for elem in asrange(0, len(array)):
            markup.add(InlineKeyboardButton(array[elem], callback_data=data[elem]))
    elif page == 1:
        async for elem in asrange(0, (list_height-1)):
            markup.add(InlineKeyboardButton(array[elem], callback_data=data[elem]))
        markup.add(InlineKeyboardButton('Следующая страница  ➡️', callback_data='next'))
    elif len(array) <= (2*(list_height-1)) + ((list_height-2) * (page - 2)):
        async for elem in asrange(((list_height-2) * (page - 2) + (list_height-1)), len(array)):
            markup.add(InlineKeyboardButton(array[elem], callback_data=data[elem]))
        markup.add(InlineKeyboardButton('⬅️ Предыдущая страница', callback_data='back'))
    else:
        async for elem in asrange(((list_height-2)*(page-2)+(list_height-1)), ((list_height-2)*(page-1)+(list_height-1))):
            markup.add(InlineKeyboardButton(array[elem], callback_data=data[elem]))
        markup.row(InlineKeyboardButton('⬅️ Предыдущая страница', callback_data='back'))
        markup.insert(InlineKeyboardButton('Следующая страница  ➡️', callback_data='next'))

    return markup
