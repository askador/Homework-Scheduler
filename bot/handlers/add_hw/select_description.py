import datetime
from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import subjects_keyboard, calendar_keyboard, subgroups_keyboard
from bot.states import SetHomework
from bot.utils.methods import clear, update_last, check_date, make_datetime, check_callback_date, check_precise
# from datetime import datetime, timedelta
from .test import ALIAS, COMMANDS


@dp.message_handler(state=SetHomework.description)
async def select_description(message: types.Message, state: FSMContext):
    hw_description = message.text

    await clear(state)

    await state.update_data(description=hw_description)
    await SetHomework.priority.set()

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Обычное', callback_data='common'))
    markup.add(InlineKeyboardButton('Важное', callback_data='important'))

    await update_last(state, await message.reply('Уточните важность задания', reply_markup=markup))