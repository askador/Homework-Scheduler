from bot.loader import dp, bot
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from aiogram.dispatcher import filters, FSMContext


@dp.inline_handler(filters.Text(startswith=['settings notifications']))
async def inline_settings_notifications(inline_query: InlineQuery):
    pins = InlineQueryResultArticle(
        id='1',
        title=f'вкл/выкл закрепление списка дз',
        input_message_content=InputTextMessageContent("pin"),
    )

    tags = InlineQueryResultArticle(
        id='2',
        title=f'вкл/выкл уведомление участников чата',
        input_message_content=InputTextMessageContent("tag"),
    )

    await bot.answer_inline_query(inline_query.id, results=[pins, tags], cache_time=1)