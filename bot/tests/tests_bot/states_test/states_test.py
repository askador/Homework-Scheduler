import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.mongo import MongoStorage

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from pymongo import MongoClient

from bot.data import config

bot = Bot(
    token=config.token,
    parse_mode=types.ParseMode.HTML,
)

mongodb_setting1 = {
    "User": "master",
    "Password": "4321",
    "Host": "chekaimat.aunqh.mongodb.net",
    "Database": "aiogram_fsm",
    "args": "retryWrites=true&w=majority"
}

db_name = config.mongodb_url[config.mongodb_url.rfind("/")+1:config.mongodb_url.rfind("?")]
storage = MongoStorage(uri=config.mongodb_url.replace(db_name, "aiogram_fsm"))


dp = Dispatcher(
    bot=bot,
    storage=storage,
)


# States
class AddChat(StatesGroup):
    subjects = State()
    subgroups = State()


@dp.message_handler(commands='start')
async def cmd_start(message):
    # Set state
    await AddChat.subjects.set()

    await message.reply("Дарова щеглы, какие предметы у вас есть?")


@dp.message_handler(state=AddChat.subjects)
async def process_name(message, state):

    async with state.proxy() as data:
        data['subjects'] = message.text

    await AddChat.next()
    await message.reply("How old are you?")


class SetHomework(StatesGroup):
    subject = State()
    name = State()
    deadline = State()
    description = State()


class GetHomework(StatesGroup):
    subject = State()
    name = State()
    deadline = State()
    description = State()


class Settings(StatesGroup):
    choice = State()
    subjects = State()
    subgroups = State()
    notifications = State()
    terms = State()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(
        dp, skip_updates=True
    )