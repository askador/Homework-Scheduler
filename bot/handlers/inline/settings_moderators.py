from bot.loader import dp, bot
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from aiogram.dispatcher import filters


@dp.inline_handler(filters.Text(startswith=['settings moderators']))
async def inline_settings_moderators(inline_query: InlineQuery):
    add = InlineQueryResultArticle(
        id='1',
        title=f'add: управление операторами',
        input_message_content=InputTextMessageContent("add"),
    )

    remove = InlineQueryResultArticle(
        id='2',
        title=f'remove: настройки уведомления',
        input_message_content=InputTextMessageContent("remove"),
    )

    await bot.answer_inline_query(inline_query.id, results=[add, remove], cache_time=1)