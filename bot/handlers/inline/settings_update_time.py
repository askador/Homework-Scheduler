from bot.loader import dp, bot
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from aiogram.dispatcher import filters, FSMContext
from bot.tests.tests_bot.states_test.states_test import InlineSettings
from bot.keyboards import select_time_keyboard
import datetime


@dp.inline_handler(filters.Text(startswith=['settings update_time']))
@dp.inline_handler(filters.Text(startswith=['settings update_time']), state=InlineSettings.update_time)
async def inline_settings_update_time(inline_query: InlineQuery, state: FSMContext):
    args = inline_query.query.split()
    await state.finish()

    text = "Выбрать новое время обновления"

    if len(args) >= 3:
        try:
            datetime.datetime.strptime(args[2], '%H')
            await InlineSettings.update_time.set()
        except Exception as e:
            text = "неправильно введено время"

    time = InlineQueryResultArticle(
            id='1',
            title=text,
            input_message_content=InputTextMessageContent(text),
    )

    await bot.answer_inline_query(inline_query.id, results=[time], cache_time=1)