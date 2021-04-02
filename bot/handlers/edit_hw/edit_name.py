from bot.loader import dp, bot
from aiogram.dispatcher import filters, FSMContext
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import subjects_keyboard, edit_hw_keyboard, calendar_keyboard, subgroups_keyboard
from bot.states import GetHomework
from bot.utils.methods import clear, update_last, check_date, make_datetime, check_callback_date, check_precise
import datetime
from .test import COMMANDS, ALIAS
from bot.types.MongoDB.Collections import Chat

SUBGROUPS = []


@dp.message_handler(state=GetHomework.name)
async def edit_name(message, state: FSMContext):
    global SUBGROUPS
    SUBGROUPS = await Chat(message.chat.id).get_subgroups()
    hw_name = message.text

    await clear(state)

    await state.update_data(name=hw_name, page=1)
    await GetHomework.next()
    markup = await subgroups_keyboard(SUBGROUPS, 1)
    await update_last(state, await message.reply("Выберите подгруппу или введите ее:", reply_markup=markup))


