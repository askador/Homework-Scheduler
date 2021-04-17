import logging

from aiogram.utils import executor
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from bot.tests.tests_bot.loader import bot, dp


@dp.inline_handler()
async def show_hw(inline_query):
    results = []
    not_found = InlineQueryResultArticle(
        title="По запросу ничего не нашлось",
        id='0',
        description='',
        input_message_content=InputTextMessageContent(message_text="По запросу ничего не нашлось")
    )
    results.append(not_found)

    await inline_query.answer(results=results, cache_time=0)


@dp.chosen_inline_handler()
async def chosen_delete_hw(chosen_inline_query):
    print(chosen_inline_query)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(
        dp, skip_updates=True
    )
