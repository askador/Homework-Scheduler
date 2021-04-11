from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import filters

from bot.data.commands.settings import COMMANDS, ALIAS
from bot.data import config
from bot.states import Settings

from bot.tests.tests_bot.settings.settings_keyboard import settings_keyboard
from bot.tests.tests_bot.settings.settings_choice import callback_select_setting

import logging

logging.basicConfig(level=logging.INFO)
bot = Bot(token = config.token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=COMMANDS)
async def settings(message):
    markup = await settings_keyboard()
    await Settings.choice.set()
    await message.reply("Настройки", reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'back', state=Settings.all_states)
async def back_to_choice(callback_query, state):
    await Settings.choice.set()
    markup = await settings_keyboard()
    await bot.edit_message_text("Меню настроек",
                                callback_query.message.chat.id,
                                callback_query.message.message_id,
                                reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'done', state=Settings.all_states)
async def back_to_choice(callback_query, state):
    await state.finish()
    await bot.edit_message_text("Удачно завершено",
                                callback_query.message.chat.id,
                                callback_query.message.message_id)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
