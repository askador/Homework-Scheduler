from bot.loader import dp, bot
from aiogram.dispatcher import filters, FSMContext
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import subjects_keyboard, edit_hw_keyboard, calendar_keyboard, subgroups_keyboard
from bot.states import GetHomework
from bot.utils.methods import clear, update_last, check_date, make_datetime, check_callback_date, check_precise
import datetime
from .test import TEST, COMMANDS, ALIAS


@dp.message_handler(state=GetHomework.description)
async def edit_description(message, state: FSMContext):
    await clear(state)
    await state.update_data(description=message.text)
    markup = await edit_hw_keyboard()
    await update_last(state, await message.reply("Описание успешно изменено!", reply_markup=markup))
    await GetHomework.choice.set()