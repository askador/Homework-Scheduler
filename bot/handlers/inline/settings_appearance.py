from bot.loader import dp, bot
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from aiogram.dispatcher import filters, FSMContext


@dp.inline_handler(filters.Text(startswith=['settings appearance']))
async def inline_settings_appearance(inline_query: InlineQuery, state: FSMContext):

    await state.finish()

    photo = InlineQueryResultArticle(
        id='1',
        title=f'вкл/выкл фото-дз',
        input_message_content=InputTextMessageContent("photo_mode"),
    )

    simple = InlineQueryResultArticle(
        id='2',
        title=f'вкл/выкл строгий режим',
        input_message_content=InputTextMessageContent("simple_mode"),
    )

    await bot.answer_inline_query(inline_query.id, results=[photo, simple], cache_time=1)