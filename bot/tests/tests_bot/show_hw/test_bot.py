import logging
import os
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text

from bot.loader import config
from generate_png import generate_png


bot = Bot(
    token=config.token,
    parse_mode=types.ParseMode.HTML,
)

dp = Dispatcher(
    bot=bot,
)


@dp.message_handler(Text(equals="скинь нюдсы"))
async def show_png(msg):
    chat_id = msg.chat.id
    html_file = f"{datetime.timestamp(datetime.now())}_{chat_id}.html"
    photo_file = f"{datetime.timestamp(datetime.now())}_{str(chat_id)}.png"

    from html_wrap import top, body, bottom

    html = top
    html += body
    html += bottom

    file = open(html_file, "w")
    file.write(html)
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
