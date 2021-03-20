import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text

from generate_png import generate_png

token = '1173133322:AAG_E7H2IjRypO3dt-pygUjh9V1HP8X8JPk' # test_bot
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
