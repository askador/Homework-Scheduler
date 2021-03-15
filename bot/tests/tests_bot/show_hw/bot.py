import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text

from generate_png import generate_png

token = '1482334694:AAH6GzEuYH34ZOwuoXgZttO87lcP9WiH_B8'
bot = Bot(
    token=token,
    parse_mode=types.ParseMode.HTML,
)

dp = Dispatcher(
    bot=bot,
)


@dp.message_handler(Text(equals="скинь нюдсы"))
async def show_png(msg):
    hw = await generate_png()
    await bot.send_photo(msg.chat.id, hw, reply_to_message_id=msg.message_id)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(
        dp, skip_updates=True
    )
