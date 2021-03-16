import logging
import os
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text, Command
from aiogram.contrib.fsm_storage.mongo import MongoStorage

from bot.loader import config
from generate_png import generate_png


bot = Bot(
    token=config.test_bot_token,
    parse_mode=types.ParseMode.HTML,
)


storage = MongoStorage(uri=config.mongodb_url)
dp = Dispatcher(
    bot=bot,
    storage=storage
)


@dp.message_handler(Text(equals="добавить дз"))
@dp.message_handler(Command(commands='add_hw'))
async def add_hw(msg):
    pass


@dp.message_handler(Text(equals="показать дз"))
async def show_png(msg):
    chat_id = msg.chat.id
    html_file = f"{datetime.timestamp(datetime.now())}_{chat_id}.html"
    photo_file = f"{datetime.timestamp(datetime.now())}_{str(chat_id)}.png"

    from generate_body import generate_body

    file = open(html_file, "w")
    file.write(generate_body({1: 1}))
    file.close()

    hw = await generate_png(html_file=html_file, output=photo_file)
    await bot.send_photo(msg.chat.id, hw, reply_to_message_id=msg.message_id)

    os.remove(html_file)
    os.remove(photo_file)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(
        dp, skip_updates=True
    )
