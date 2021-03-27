from .process_subgroups import process_subgroups
from .process_subjects import process_subjects

from bot.loader import dp, bot
from bot.scheduler import scheduler
from aiogram import types
from aiogram.dispatcher import filters
from bot.tests.tests_bot.states_test.states_test import AddChat
from bot.utils.methods import show_hw
from .test import CHAT_TYPES


@dp.message_handler(filters.ChatTypeFilter(CHAT_TYPES), commands=['start'], is_chat_admin=True)
async def start(message):
    await AddChat.subjects.set()
    await message.reply("Привет, я Homework Scheduler! Сейчас начнется моя настройка!"
                               "\n"
                               "Предметы через запятую, быстро")