from aiogram import Bot,Dispatcher, executor
from bot.data import config
import logging

from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle
from bot.keyboards import homework_kb_both

from bot.types import HomeworksList, Database
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
bot = Bot(token = config.test_bot_token)
dp = Dispatcher(bot)


@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    chat_id = -1001424619068

    text = inline_query.query or 'echo'
    homework_info = InputTextMessageContent("sjhfjsfd____")
    result_id = '56'
    item1 = InlineQueryResultArticle(
        id=result_id,
        title=f'1',
        description="sjfdgjdfg",
        input_message_content=homework_info,
    )
    item2 = InlineQueryResultArticle(
        id=result_id+"1",
        title=f'2',
        description="sjfdgjdfg",
        input_message_content=homework_info,
    )
    # don't forget to set cache_time=1 for testing (default is 300s or 5m)
    a = await bot.answer_inline_query(inline_query_id=inline_query.id, switch_pm_text="ssdfsd", switch_pm_parameter="_",
                       results=[item1, item2], cache_time=0)
    print(a)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

