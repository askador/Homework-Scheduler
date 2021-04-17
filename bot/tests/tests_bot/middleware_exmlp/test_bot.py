import asyncio
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler, SkipHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled

from bot.tests.tests_bot.loader import bot, dp
from bot.types import Database

logging.basicConfig(level=logging.INFO)





@dp.message_handler(commands=['start'])
async def cmd_test(message: types.Message):
    # You can use this command every 5 seconds
    await message.reply('Test passed! You can use this command every 5 seconds.')


if __name__ == '__main__':
    dp.middleware.setup(ChatAmount())
    executor.start_polling(dp)