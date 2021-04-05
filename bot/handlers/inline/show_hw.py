from bot.loader import dp, bot
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from aiogram.dispatcher import filters, FSMContext
from bot.utils.methods import check_date
from bot.states import Inline


@dp.inline_handler(filters.Text(startswith=['show_hw']))
async def inline_show(inline_query: InlineQuery, state: FSMContext):
    args = inline_query.query.split()

    hw = 'loading...'
    item = None

    if len(args) == 1:
        hw = 'зручний пошук такої незручної домашки)'
    else :
        hw = 'давай Серега, давай'

    input_content = InputTextMessageContent(hw, parse_mode='HTML')
    result_id = '1'
    item = InlineQueryResultArticle(
        title='show_hw:',
        id=result_id,
        description=f'{hw!r}',
        input_message_content=input_content,
    )

    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)