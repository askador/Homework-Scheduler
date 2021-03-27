from .edit_deadline import edit_deadline
from .edit_description import edit_description
from .edit_name import edit_name
from .edit_subject import edit_subject
from .edit_subgroup import edit_subgroup
from .edit_choice import edit_choice

from bot.loader import dp, bot
from aiogram.dispatcher import filters, FSMContext
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import subjects_keyboard, edit_hw_keyboard, calendar_keyboard, subgroups_keyboard
from bot.tests.tests_bot.states_test.states_test import GetHomework
from bot.utils.methods import clear, update_last, check_date, make_datetime, check_callback_date, check_precise
import datetime
from .test import TEST, COMMANDS, ALIAS


@dp.message_handler(commands=COMMANDS,  is_chat_admin=True)
@dp.message_handler(filters.Text(startswith=ALIAS),  is_chat_admin=True)
async def edit_hw(message):
    try:
        arguments = message.get_args().split()
    except Exception as e:
        arguments = None

    print(arguments)
    text = "Выберите предмет или введите его:"

    if arguments is not None and len(arguments) >= 2:
        if arguments[0] in TEST:
            return await message.reply("все сразу, круто")
        else:
            text = "Введенные данные не подходят, вызываю стандартный диалог.\nВыберите предмет или введите его:"
    elif arguments is None:
        arguments = message.text.split()
        if len(arguments) > 2 and arguments[2] in TEST:
            return await message.reply("все сразу, круто")
        else:
            text = "Введенные данные не подходят, вызываю стандартный диалог.\nВыберите предмет или введите его:"

    await GetHomework.subject.set()
    state = dp.get_current().current_state()
    await state.update_data(page=1)
    markup = await subjects_keyboard(TEST, 1)
    await update_last(state, await message.reply(text, reply_markup=markup))

