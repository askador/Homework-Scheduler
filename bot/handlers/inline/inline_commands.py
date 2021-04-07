from bot.loader import dp, bot
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from aiogram.dispatcher import FSMContext


@dp.inline_handler()
async def inline_commands(inline_query: InlineQuery, state: FSMContext):
    await state.finish()

    hw = InlineQueryResultArticle(
        id='1',
        title=f'дз: показать дз',
        input_message_content=InputTextMessageContent("дз"),
    )

    add_hw = InlineQueryResultArticle(
        id='2',
        title=f'add_hw: добавить дз',
        input_message_content=InputTextMessageContent("add_hw"),
    )

    edit_hw = InlineQueryResultArticle(
        id='3',
        title=f'edit_hw: изменить дз',
        input_message_content=InputTextMessageContent("edit_hw"),
    )

    del_hw = InlineQueryResultArticle(
        id='4',
        title=f'del_hw: удалить дз',
        input_message_content=InputTextMessageContent("del_hw"),
    )

    settings = InlineQueryResultArticle(
        id='5',
        title=f'settings: настройки чата',
        input_message_content=InputTextMessageContent("settings"),
    )

    await bot.answer_inline_query(inline_query.id, results=[hw, add_hw, edit_hw, del_hw, settings], cache_time=1)