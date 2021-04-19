from bot.loader import dp, bot
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from aiogram.dispatcher import filters, FSMContext
from aiogram.utils.exceptions import InvalidQueryID
from bot.utils.methods import check_date
from bot.states import Inline
from bot.utils.methods import user_in_chat_students
from bot.types.MongoDB import Chat

IMAGES = {
    "add_hw" : "https://i.imgur.com/OTKZVgd.png",
    "cancel" : "https://i.imgur.com/2iiesoE.png"
}

OUTPUTS = {
    "0": {
        "description": "Загрузка...",
        "input": "Я молодец и неправильно ввел аргументы",
        "url": IMAGES["add_hw"]
    },
    "1": {
        "description": "предмет, название, подгруппа, срок_сдачи",
        "input": "Я молодец и неправильно ввел аргументы",
        "url": IMAGES["add_hw"]
    },
    "2": {
        "description": "Успешно заполнено!",
        "input": "Типа добавляем",
        "url": IMAGES["add_hw"]
    },
    "3": {
        "description": "Подгруппа введена неверно!",
        "input": "Недописал и кликнул",
        "url": IMAGES["cancel"]
    },
    "4": {
        "description": "Дата введена неверно!",
        "input": "Недописал и кликнул",
        "url": IMAGES["cancel"]
    },
    "5": {
        "description": "Предмет введен неверно!",
        "input": "Недописал и кликнул",
        "url": IMAGES["cancel"]
    },

}


@dp.inline_handler(filters.Text(startswith=['add_hw']))
async def inline_add_hw(inline_query: InlineQuery):

    id = 1

    chat_id = await user_in_chat_students(inline_query.from_user.id)
    if not chat_id:
        await inline_query.answer(results=[
            InlineQueryResultArticle(
                title='Показать дз',
                id='1',
                description='Вы не привязаны к группе!\n'
                            'Воспользуйтесь ботом в чате, куда вы хотите получать ответ',
                input_message_content=InputTextMessageContent(
                    message_text='Вы не привязаны к группе!\n'
                                 'Воспользуйтесь ботом в чате, куда вы хотите получать ответ'
                )
            )
        ],
            cache_time=0)
        return

    args = inline_query.query.replace("add_hw", "").split(",")
    args = [arg.strip() for arg in args]

    #print(args)

    subjects = await Chat(chat_id).get_field_value('subjects')
    subgroups = await Chat(chat_id).get_field_value('subjects')

    key = "0"
    cache = []

    if len(args) == 1:
        key = "1"
    elif len(args) >= 1:
        if args[0] in subjects:
            key = "1"
            if len(args) >= 3:
                if args[2] in subgroups or args[2] == 'все':
                    pass
                else:
                    key = "3"
                if len(args) >= 4:
                    if await check_date([args[3]]):
                        key = "2"
                        cache = args
                        cache.append("from inline")
                        cache.append("common")
                    else:
                        key = "4"
                else:
                    pass
            else:
                pass
        else:
            key = "5"
    else:
        pass

    if key == "2":
        OUTPUTS[key]["input"] = "add_hw {}, {}, {}, {}, {}, {}".format(*cache)

    input_content = InputTextMessageContent(OUTPUTS[key]["input"], parse_mode='HTML')
    result_id = '{}'.format(id)
    item = InlineQueryResultArticle(
        title='add_hw:',
        id=result_id,
        description=f'{OUTPUTS[key]["description"]!r}',
        input_message_content=input_content,
        thumb_url=OUTPUTS[key]["url"], thumb_height=32, thumb_width=32
    )

    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)

    """try:
        await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)
    except InvalidQueryID:
        await bot.send_message(chat_id,
                               text="Время ожидания инлайн запроса истекло.\n"
                                    "Удалите и напишите запрос снова")"""
