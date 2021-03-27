from bot.loader import dp, bot
from bot.scheduler import scheduler
from aiogram import types
from aiogram.dispatcher import filters
from bot.tests.tests_bot.states_test.states_test import AddChat
from bot.utils.methods import show_hw


CHAT_TYPES = [
    types.ChatType.GROUP,
    types.ChatType.SUPERGROUP
]