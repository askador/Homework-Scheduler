import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.data import config
from bot.types.MongoDB.Database import Database

bot = Bot(
    token=config.token,
    parse_mode=types.ParseMode.HTML,
)

db_name = config.mongodb_url[config.mongodb_url.rfind("/") + 1:config.mongodb_url.rfind("?")]
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
    await AddChat.subjects.set()

    await message.reply("Дарова щеглы, какие предметы у вас есть?\n"
                        "Через запятку ввел быро")


@dp.message_handler(lambda mes: not mes.text.isdigit(), state=AddChat.subjects)
async def process_name(message, state):
    async with state.proxy() as data:
        data['subjects'] = message.text
        data['subjects_amount'] = len(message.text.split(','))

        await AddChat.next()
        await message.reply("Акей, теперь введи для каждого предмета список подгрупп\n"
                            "Если таких нет, просто нажми на кнопку `пойти нахуй`")
        await message.answer(f"Количество подгрупп для {data['subjects'].split(',')[0]}")


@dp.message_handler(lambda mes: mes.text.isdigit(), state=AddChat.subgroups)
async def process_name(message, state):
    async with state.proxy() as data:
        subjects = data['subjects'].split(',')
        data['subjects_amount'] -= 1
        data[subjects[data['subjects_amount']]] = message.text
        if data['subjects_amount'] == 0:
            await message.answer("Мб не будешь хыуйней заниматься?")
            await message.answer(data)
            db = Database()
            db.delete("aiogram_data", {"chat": message.chat.id})
            await state.reset_state(with_data=True)
        else:
            await message.answer(f"Количество подгрупп для {subjects[data['subjects_amount']].strip()}")
            # await message.answer(f"{subjects[data['subjects_amount']]}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # utils.setup_logger("INFO", ["sqlalchemy.engine", "aiogram.bot.api"])
    executor.start_polling(
        dp, skip_updates=True
    )
