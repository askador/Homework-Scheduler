from bot.loader import dp, bot
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from aiogram.dispatcher import filters


@dp.inline_handler()
async def inline(inline_query):
    print(inline_query)

