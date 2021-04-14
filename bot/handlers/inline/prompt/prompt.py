from bot.loader import dp, bot
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from aiogram.dispatcher import filters, FSMContext

OUTPUTS = [
    {
        "title": "add_hw",
        "description": "Добавить дз",
        "input": "Нажал на подсказку",
        "url": "https://i.imgur.com/f5uscGB.png"
    },
    {
        "title": "edit_hw",
        "description": "Изменить дз",
        "input": "Нажал на подсказку",
        "url": "https://i.imgur.com/TgRtSFO.png"
    },
   {
        "title": "del_hw",
        "description": "Удалить дз",
        "input": "Нажал на подсказку",
        "url": "https://i.imgur.com/godfTeT.png"
    },
    {
        "title": "show_hw",
        "description": "Показать дз",
        "input": "Нажал на подсказку",
        "url": "https://i.imgur.com/ZNlIlT0.png"
    },
]


@dp.inline_handler(filters.Text(equals=""))
async def inline_prompt(inline_query: InlineQuery, state: FSMContext):

    id = 1
    items = []
    for output in OUTPUTS:

        input_content = InputTextMessageContent(output["input"], parse_mode='HTML')
        result_id = '{}'.format(id)
        item = InlineQueryResultArticle(
            title=output["title"],
            id=result_id,
            description=f'{output["description"]!r}',
            input_message_content=input_content,
            thumb_url=output["url"], thumb_height=32, thumb_width=32
        )
        items.append(item)
        id += 1

    await bot.answer_inline_query(inline_query.id, results=items, cache_time=1)
