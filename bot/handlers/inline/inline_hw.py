from bot.loader import dp, bot
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from aiogram.dispatcher import filters


@dp.inline_handler(filters.Text(startswith=['дз']))
async def inline_hw(inline_query: InlineQuery):
    hw = 'купи слона'
    input_content = InputTextMessageContent(hw)
    result_id = '1'
    item = InlineQueryResultArticle(
        title="ДЗ:",
        id=result_id,
        description=f'{hw!r}',
        input_message_content=input_content,
    )
    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)