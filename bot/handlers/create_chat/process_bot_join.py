from bot.loader import bot, dp
from bot.states import AddChat
from bot.utils.methods import get_chat_admins
from bot.types import Database


@dp.message_handler(content_types=["new_chat_members"])
async def process_bot_join(message, state):
    print(message)
    chat_id = message.chat.id

    db = Database()
    already_exists = await db.find(collection="chat", filters={"_id": chat_id})

    if already_exists:
        return

    for user in message.new_chat_members:
        if user.id == bot.id:
            chat_title = message.chat.title
            chat_admins = await get_chat_admins(chat_id)

            await AddChat.subjects.set()

            async with state.proxy() as data:
                data['chat_id'] = chat_id
                data['chat_title'] = chat_title
                data['chat_admins'] = chat_admins

            await message.answer("Привет, я Homework Scheduler! \n"
                                 "Сейчас начнется моя настройка!\n"
                                 "Пожалуйста введите список ваших предметов через запятую")

            return
