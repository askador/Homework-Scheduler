from bot.loader import dp, bot
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from aiogram.dispatcher import filters, FSMContext
from bot.utils.methods import edit_parse_hw
from bot.states import Inline

TEST = [
    '1'
]


@dp.inline_handler(filters.Text(startswith=['edit_hw']))
@dp.inline_handler(filters.Text(startswith=['edit_hw']))
async def inline_edit_hw(inline_query: InlineQuery, state: FSMContext):

    hw = "Надо дзхи сюда"
    input = "Типа реагирует на это бот"

    input_content = InputTextMessageContent(input)
    result_id = '1'
    item = InlineQueryResultArticle(
        title='edit_hw:',
        id=result_id,
        description=f'{hw!r}',
        input_message_content=input_content,
        thumb_url="https://i.imgur.com/TgRtSFO.png", thumb_height=32, thumb_width=32
    )
    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)