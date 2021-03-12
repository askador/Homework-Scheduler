from bot.loader import dp, bot


@dp.message_handler(lambda msg: msg.text.lower() == "админы")
async def get_chat_admins(msg):
    admins_object = await bot.get_chat_administrators(msg.chat.id)

    admins_list = []

    for admin in admins_object:
        admins_list.append(admin.user.id)

    await msg.answer(str(admins_list))
