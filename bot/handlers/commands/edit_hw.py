from pprint import pprint

from bot.loader import dp, bot
from aiogram.dispatcher import filters, FSMContext
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import subjects_keyboard, edit_hw_keyboard, calendar_keyboard, subgroups_keyboard
from bot.states import GetHomework
from bot.utils.methods import clear, update_last, check_date, make_datetime, check_callback_date, check_precise
import datetime
from bot.data.commands.edit_hw import COMMANDS, ALIAS
from bot.types.MongoDB.Collections import Chat

from bot.utils.methods.generate_hws_kb import generate_hws_kb


@dp.message_handler(commands=COMMANDS,  is_chat_admin=True)
@dp.message_handler(filters.Text(startswith=ALIAS),  is_chat_admin=True)
async def edit_hw(message):
    chat_id = message.chat.id

    chat = Chat(chat_id)

    homeworks = await chat.get_homeworks(filters=[{}], full_info=False)

    kb = await generate_hws_kb(homeworks)
    await message.answer(text="Выберите задание, которое Вы хотите редактировать",
                         reply_markup=kb)


    """
    SUBJECTS = await Chat(message.chat.id).get_field_value("subjects")

    try:
        arguments = message.get_args().split()
    except Exception as e:
        arguments = None

    # print(arguments)
    text = "Выберите предмет или введите его:"

    if arguments is not None and len(arguments) >= 2:
        if arguments[0] in SUBJECTS:
            return await message.reply("все сразу, круто")
        else:
            text = "Введенные данные не подходят, вызываю стандартный диалог.\nВыберите предмет или введите его:"
    elif arguments is None:
        arguments = message.text.split()
        if len(arguments) > 2 and arguments[2] in SUBJECTS:
            return await message.reply("все сразу, круто")
        else:
            text = "Введенные данные не подходят, вызываю стандартный диалог.\nВыберите предмет или введите его:"

    await GetHomework.subject.set()
    state = dp.get_current().current_state()
    await state.update_data(page=1)
    markup = await subjects_keyboard(SUBJECTS, 1)
    await update_last(state, await message.reply(text, reply_markup=markup))
    """


