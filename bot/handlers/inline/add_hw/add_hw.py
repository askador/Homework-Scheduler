from bot.loader import dp, bot
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from aiogram.dispatcher import filters, FSMContext
from bot.utils.methods import check_date
from bot.states import Inline


TEST = [
    "1"
]

OUTPUTS = {
    "0": {
        "description": "Загрузка...",
        "input": "Я молодец и неправильно ввел аргументы",
        "url": "https://i.imgur.com/f5uscGB.png"
    },
    "1": {
        "description": "предмет название подгруппа срок_сдачи",
        "input": "Я молодец и неправильно ввел аргументы",
        "url": "https://i.imgur.com/f5uscGB.png"
    },
    "2": {
        "description": "Успешно заполнено!",
        "input": "Типа добавляем",
        "url": "https://i.imgur.com/f5uscGB.png"
    },
    "3": {
        "description": "Подгруппа введена неверно!",
        "input": "Недописал и кликнул",
        "url": "https://i.imgur.com/2iiesoE.png"
    },
    "4": {
        "description": "Дата введена неверно!",
        "input": "Недописал и кликнул",
        "url": "https://i.imgur.com/2iiesoE.png"
    },
    "5": {
        "description": "Предмет введен неверно!",
        "input": "Недописал и кликнул",
        "url": "https://i.imgur.com/2iiesoE.png"
    },

}


@dp.inline_handler(filters.Text(startswith=['add_hw']))
@dp.inline_handler(filters.Text(startswith=['add_hw']))
async def inline_add_hw(inline_query: InlineQuery, state: FSMContext):
    # state = dp.get_current().current_state()
    await state.finish()

    args = inline_query.query.split()

    key = "0"

    if len(args) == 1:
        key = "1"
    elif len(args) >= 2:
        if args[1] in TEST:
            key = "1"
            if len(args) >=4:
                if args[3] in TEST or args[3] == 'все':
                    pass
                else:
                    key = "3"
                if len(args) >= 5:
                    if await check_date([args[4]]):
                        key = "2"
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

    input_content = InputTextMessageContent(OUTPUTS[key]["input"], parse_mode='HTML')
    result_id = '1'
    item = InlineQueryResultArticle(
        title='add_hw:',
        id=result_id,
        description=f'{OUTPUTS[key]["description"]!r}',
        input_message_content=input_content,
        thumb_url=OUTPUTS[key]["url"], thumb_height=32, thumb_width=32
    )

    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)