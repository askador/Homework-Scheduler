from bot.loader import dp
from bot.scheduler import scheduler
from aiogram.types import ChatType
from aiogram.dispatcher.filters import ChatTypeFilter
from bot.states import AddChat
from bot.utils.methods import get_chat_admins
from bot.types import Database

CHAT_TYPES = [
    ChatType.GROUP,
    ChatType.SUPERGROUP
]


@dp.message_handler(ChatTypeFilter(CHAT_TYPES), commands=['start'], is_chat_admin=True, state="*")
async def start(message, state):
    chat_id = message.chat.id

    db = Database()
    already_exists = await db.find(collection="chat", filters={"_id": chat_id})

    if already_exists:
        return 0

    chat_title = message.chat.title
    chat_admins = await get_chat_admins(chat_id)

    await AddChat.subjects.set()

    async with state.proxy() as data:
        data['chat_id'] = chat_id
        data['chat_title'] = chat_title
        data['chat_admins'] = chat_admins


    await message.answer("Привет, я Homework Scheduler! \nСейчас начнется моя настройка!\n"
                         "Пожалуйста введите список ваших предметов через запятую")
