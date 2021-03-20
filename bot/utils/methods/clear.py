from bot.loader import bot


async def clear(state):
    try:
        async with state.proxy() as data:
            d_id = data['last_message_id']

        await bot.delete_message(state.chat, d_id)
    except Exception as e:
        pass