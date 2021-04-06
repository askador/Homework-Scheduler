from bot.data.commands.add_hw import ALIAS, COMMANDS

from bot.loader import dp
from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import subjects_keyboard, list_keyboard, calendar_keyboard, subgroups_keyboard
from bot.states import SetHomework
from bot.utils.methods import clear, update_last, check_date, make_datetime, check_callback_date, check_precise
from bot.types.MongoDB.Collections import Chat


@dp.message_handler(commands=COMMANDS,  access_level='moderator')
@dp.message_handler(filters.Text(startswith=ALIAS),  access_level='moderator')
async def add_hw(message: types.Message):
    try:
        arguments = message.get_args().split()
    except Exception as e:
        arguments = None

    SUBJECTS = await Chat(message.chat.id).get_field_value("subjects")

    text = "Выберите предмет или введите его:"

    if arguments is not None and len(arguments) >= 3:
        if arguments[0] in SUBJECTS and await check_date(arguments[2]):
            return await message.reply("все сразу, круто")
        else:
            text = "Введенные данные не подходят, вызываю стандартный диалог.\nВыберите предмет или введите его:"
    elif arguments is None:
        arguments = message.text.split()
        if len(arguments) > 2 and arguments[2] in SUBJECTS and await check_date(arguments[4]):
            return await message.reply("все сразу, круто")
        else:
            text = "Введенные данные не подходят, вызываю стандартный диалог.\nВыберите предмет или введите его:"

    await SetHomework.subject.set()
    state = dp.get_current().current_state()
    await state.update_data(page=1)

    markup = await list_keyboard(message.chat.id, 'subject', 1)
    await update_last(state, await message.reply(text, reply_markup=markup))