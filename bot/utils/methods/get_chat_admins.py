from bot.loader import bot


async def get_chat_admins(chat_id):
    admins_object = await bot.get_chat_administrators(chat_id)

    admins_list = []

    for admin in admins_object:
        admins_list.append(int(admin.user.id))

    return admins_list
