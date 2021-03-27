from bot.loader import dp, bot
from bot.scheduler import scheduler
from aiogram import types
from aiogram.dispatcher import filters
from bot.tests.tests_bot.states_test.states_test import AddChat
from bot.utils.methods import show_hw
from .test import CHAT_TYPES


@dp.message_handler(filters.ChatTypeFilter(CHAT_TYPES), state=AddChat.subjects)
async def process_subjects(message, state):

    async with state.proxy() as data:
        data['subjects'] = message.text

    await AddChat.next()
    await message.reply("Теперь перечислите подгруппы, отправьте None если их нет")