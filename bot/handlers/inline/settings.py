from bot.loader import dp, bot
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from aiogram.dispatcher import filters, FSMContext


@dp.inline_handler(filters.Text(startswith=['settings']))
async def inline_settings(inline_query: InlineQuery):


    moderators = InlineQueryResultArticle(
        id='1',
        title=f'moderators: управление операторами',
        input_message_content=InputTextMessageContent("moderators"),
    )

    notifications = InlineQueryResultArticle(
        id='2',
        title=f'notifications: настройки уведомления',
        input_message_content=InputTextMessageContent("notifications"),
    )

    update_time = InlineQueryResultArticle(
        id='3',
        title=f'update_time: выбрать время ',
        input_message_content=InputTextMessageContent("update_time"),
    )

    appearance = InlineQueryResultArticle(
        id='4',
        title=f'appearance: настройки отображения ',
        input_message_content=InputTextMessageContent("appearance"),
    )

    await bot.answer_inline_query(inline_query.id, results=[moderators, notifications, update_time, appearance], cache_time=1)