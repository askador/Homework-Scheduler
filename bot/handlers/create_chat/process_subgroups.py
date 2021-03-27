from bot.loader import dp, bot
from bot.scheduler import scheduler
from aiogram import types
from aiogram.dispatcher import filters
from bot.tests.tests_bot.states_test.states_test import AddChat
from bot.utils.methods import show_hw
from .test import CHAT_TYPES


@dp.message_handler(filters.ChatTypeFilter(CHAT_TYPES), state=AddChat.subgroups)
async def process_subgroups(message, state):

    async with state.proxy() as data:
        data['subgroups'] = message.text

    await state.finish()
    # scheduler.add_job(show_hw, 'cron', hour=15, minute=19, args={message}) добавить в список определенного времени
    await message.reply("Бот запущен с такими настройками:")