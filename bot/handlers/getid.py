from bot.loader import dp


@dp.message_handler(lambda msg: msg.reply_to_message is not None and msg.text.lower() == "getid")
async def get_id(msg):
    try:
        await msg.reply(msg.reply_to_message.from_user.id)
    except Exception:
        pass
