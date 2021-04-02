from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from bot.states import DeleteHomework
from bot.keyboards import subjects_keyboard, subgroups_keyboard
from bot.utils.methods import update_last, clear
from bot.handlers.del_hw.test import COMMANDS
from bot.types.MongoDB.Collections import Chat

SUBJECTS = []


@dp.message_handler(commands=COMMANDS,  is_chat_admin=True)
async def delete_hw(message: types.Message):

    global SUBJECTS
    SUBJECTS = await Chat(message.chat.id).get_subjects()

    markup = await subjects_keyboard(SUBJECTS, 1)
    await DeleteHomework.subject.set()
    state = dp.get_current().current_state()
    await state.update_data(page=1)

    await update_last(state, await message.reply('Выберите предмет задания или введите его:', reply_markup=markup))