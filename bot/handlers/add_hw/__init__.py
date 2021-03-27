from .select_subject import select_subject
from .select_deadline import select_deadline
from .select_description import select_description
from .select_name import select_name
from .select_subgroup import select_subgroup
from .select_priority import set_priority


import datetime
from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import subjects_keyboard, calendar_keyboard, subgroups_keyboard
from bot.tests.tests_bot.states_test.states_test import SetHomework
from bot.utils.methods import clear, update_last, check_date, make_datetime, check_callback_date, check_precise
# from datetime import datetime, timedelta
from .test import TEST, ALIAS, COMMANDS


@dp.message_handler(commands=COMMANDS,  is_chat_admin=True)
@dp.message_handler(filters.Text(startswith=ALIAS),  is_chat_admin=True)
async def add_hw(message: types.Message):
    print(message)
    try:
        arguments = message.get_args().split()
    except Exception as e:
        arguments = None

    print(arguments)
    text = "Выберите предмет или введите его:"

    if arguments is not None and len(arguments) >= 3:
        if arguments[0] in TEST and await check_date(arguments[2]):
            return await message.reply("все сразу, круто")
        else:
            text = "Введенные данные не подходят, вызываю стандартный диалог.\nВыберите предмет или введите его:"
    elif arguments is None:
        arguments = message.text.split()
        if len(arguments) > 2 and arguments[2] in TEST and await check_date(arguments[4]):
            return await message.reply("все сразу, круто")
        else:
            text = "Введенные данные не подходят, вызываю стандартный диалог.\nВыберите предмет или введите его:"

    await SetHomework.subject.set()
    state = dp.get_current().current_state()
    await state.update_data(page=1)

    markup = await subjects_keyboard(TEST, 1)
    await update_last(state, await message.reply(text, reply_markup=markup))