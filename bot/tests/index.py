from aiogram import Bot, Dispatcher, executor
from bot.data import config
import logging

logging.basicConfig(level=logging.INFO)
bot = Bot(token = config.token)
dp = Dispatcher(bot)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

