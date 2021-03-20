from bot.loader import dp, bot
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from aiogram.dispatcher import filters


@dp.inline_handler(lambda query: len(query.query) == 0)
async def inline_commands(inline_query: InlineQuery):
    hw = InlineQueryResultArticle(
        id='1',
        title=f'дз: показать дз',
        input_message_content=InputTextMessageContent("дз"),
    )
    await bot.answer_inline_query(inline_query.id, results=[hw], cache_time=1)