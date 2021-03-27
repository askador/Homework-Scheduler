from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from bot.tests.tests_bot.states_test.states_test import DeleteHomework
from bot.keyboards import subjects_keyboard, subgroups_keyboard
from bot.utils.methods import update_last, clear
from .test import COMMANDS, TEST


@dp.message_handler(state=DeleteHomework.name)
async def delete_name(message: types.Message, state: FSMContext):
    await clear(state)

    markup = await subgroups_keyboard(TEST, 1)
    await DeleteHomework.subgroup.set()
    await state.update_data(page=1)

    await update_last(state, await message.reply('Выберите подгруппу или введите её:', reply_markup=markup))