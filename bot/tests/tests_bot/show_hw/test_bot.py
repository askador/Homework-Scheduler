import logging
import os
from datetime import datetime, timedelta

from pymongo import MongoClient
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text, Command
from aiogram.contrib.fsm_storage.mongo import MongoStorage

from bot.loader import config
from generate_png import generate_png
from bot.types.HomeworksList import HomeworksList


bot = Bot(
    token=config.test_bot_token,
    parse_mode=types.ParseMode.HTML,
)


storage = MongoStorage(uri=config.mongodb_url)
dp = Dispatcher(
    bot=bot,
    storage=storage
)


@dp.message_handler(Text(equals="добавить чат"))
async def add_chat(msg):
    chat_id = msg.chat.id
    title = msg.chat.title
    admins_object = await bot.get_chat_administrators(msg.chat.id)
    admins_list = []
    for admin in admins_object:
        admins_list.append(admin.user.id)

    chat = {"_id": chat_id, "title": title, "admins": admins_list,
             "subjects": ["apr", "matan"], "subgroups": {}, "homeworks": []}

    client = MongoClient(config.mongodb_url)
    db = client["hw_bot_db"]
    col = db["chat"]

    # col.insert_one(chat)

    await msg.reply(chat)


@dp.message_handler(Text(contains="добавить"), chat_id=526497876)
async def add_hw(msg):

    id = msg.text.split(',')[0+1]
    subj = msg.text.split(',')[1+1]
    name = msg.text.split(',')[2+1]
    description = msg.text.split(',')[3+1]
    deadline = msg.text.split(',')[4+1]
    subgroup = msg.text.split(',')[5+1]
    priority = msg.text.split(',')[6+1]

    client = MongoClient(config.mongodb_url)
    db = client["hw_bot_db"]
    col = db["chat"]

    hw = {
        "_id": id,
        "subject": subj,
        "name": name,
        "description": description,
        "deadline": deadline,
        "subgroup": subgroup,
        "priority": priority,
    }

    await msg.reply(hw)

    col.update_one({"_id": -1001424619068}, {"$push": {"homeworks": hw}})

    columns = [
        "id",
        "subject",
        "name",
        "description",
        "deadline",
        "subgroup",
        "priority",
    ]


@dp.message_handler(Text(equals="показать дз"))
async def show_png(msg):
    chat_id = msg.chat.id
    html_file = f"{datetime.timestamp(datetime.now())}_{chat_id}.html"
    photo_file = f"{datetime.timestamp(datetime.now())}_{str(chat_id)}.png"

    script_dir = os.path.dirname(__file__)
    script_dir = "/".join(script_dir.split('/')[:script_dir.split('/').index("bot") + 1])
    html = script_dir + f"/utils/html_photo/temp_photo/{html_file}"
    photo = script_dir + f"/utils/html_photo/temp_photo/{photo_file}"

    client = MongoClient(config.mongodb_url)
    db = client["hw_bot_db"]
    col = db["chat"]

    homeworks = []

    for x in col.find({"_id": -1001424619068}, {"_id": 0, "homeworks": 1}):
        homeworks = x["homeworks"]

    if not homeworks:
        await msg.reply("Домашнего задания нет")
        return

    hws_list = HomeworksList(0)
    await hws_list.set_fields(homeworks)


    hw_photo = await hws_list.generate_photo(html_file=html, photo_file=photo)
    await msg.answer_photo(hw_photo)
    os.remove(html)
    os.remove(photo)
    # await bot.send_photo(msg.chat.id, hw_photo, reply_to_message_id=msg.message_id)
    #
    # os.remove(html_file)
    # os.remove(photo_file)


@dp.message_handler(Text(equals="time"), chat_id=526497876)
async def get_time(msg):
    from datetime import datetime, time
    print(type(msg.date))
    # await msg.reply(time(int(msg.date)))
    await msg.reply(msg.date)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(
        dp, skip_updates=True
    )
