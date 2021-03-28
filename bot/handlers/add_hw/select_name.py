import datetime
from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import subjects_keyboard, calendar_keyboard, subgroups_keyboard
from bot.states import SetHomework
from bot.utils.methods import clear, update_last, check_date, make_datetime, check_callback_date, check_precise
# from datetime import datetime, timedelta
from .test import TEST, ALIAS, COMMANDS


@dp.message_handler(state=SetHomework.name)
async def select_name(message: types.Message, state: FSMContext):
    hw_name = message.text

    await clear(state)

    await state.update_data(name=hw_name)
    await SetHomework.next()
    await state.update_data(month=0)

    markup = await subgroups_keyboard(TEST, 1)
    await update_last(state, await message.reply("Выберите подгруппу:", reply_markup=markup))