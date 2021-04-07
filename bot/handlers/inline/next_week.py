from bot.loader import dp


@dp.inline_handler()
async def inline(inline_query):
    print(inline_query)

