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


@dp.message_handler(filters.ChatTypeFilter(CHAT_TYPES), commands=['start'], is_chat_admin=True)
async def command_start(message):
    await AddChat.subjects.set()
    await message.reply("Привет, я Homework Scheduler! Сейчас начнется моя настройка!"
                               "\n"
                               "Предметы через запятую, быстро")


@dp.message_handler(filters.ChatTypeFilter(CHAT_TYPES), state=AddChat.subjects)
async def process_subjects(message, state):

    async with state.proxy() as data:
        data['subjects'] = message.text

    await AddChat.next()
    await message.reply("Теперь перечислите подгруппы, отправьте None если их нет")


@dp.message_handler(filters.ChatTypeFilter(CHAT_TYPES), state=AddChat.subgroups)
async def process_subgroups(message, state):

    async with state.proxy() as data:
        data['subgroups'] = message.text

    await state.finish()
    scheduler.add_job(show_hw, 'cron', hour=15, minute=19, args={message})
    await message.reply("Бот запущен с такими настройками:")

