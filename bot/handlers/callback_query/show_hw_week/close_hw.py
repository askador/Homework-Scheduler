from bot.loader import dp, bot


@dp.callback_query_handler(lambda call: call.data == 'close', state="*")
async def close_hw(call, state):
    message_id = call.message.message_id
    chat_id = call.message.chat.id

    async with state.proxy() as data:
        data['week_page'] = 0

    await bot.delete_message(chat_id, message_id)
    await state.finish()
