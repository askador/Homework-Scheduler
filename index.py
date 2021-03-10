from aiogram import Bot,Dispatcher, executor, types
from data.config import token
import logging

logging.basicConfig(level=logging.INFO)
bot = Bot(token = token)
dp = Dispatcher(bot)


@dp.message_handler(user_id=[526497876])
async def mes(msg):
    await msg.answer("Correct")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)