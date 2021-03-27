from .del_subject import delete_subject
from .del_name import delete_name
from .del_subgroup import delete_subgroup

from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from bot.tests.tests_bot.states_test.states_test import DeleteHomework
from bot.keyboards import subjects_keyboard, subgroups_keyboard
from bot.utils.methods import update_last, clear
from .test import COMMANDS, TEST


@dp.message_handler(commands=COMMANDS,  is_chat_admin=True)
async def delete_hw(message: types.Message):
    markup = await subjects_keyboard(TEST, 1)
    await DeleteHomework.subject.set()
    state = dp.get_current().current_state()
    await state.update_data(page=1)

    await update_last(state, await message.reply('Выберите предмет задания или введите его:', reply_markup=markup))