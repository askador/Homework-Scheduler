from bot.loader import dp, bot
from aiogram.dispatcher import filters, FSMContext
from aiogram import types
from bot.keyboards import select_time_keyboard, settings_keyboard_appearance, settings_keyboard_moderators, settings_keyboard, settings_keyboard_subjects, settings_keyboard_subgroups, settings_keyboard_notifications, settings_keyboard_terms
from bot.tests.tests_bot.states_test.states_test import Settings
from bot.utils.methods import clear, update_last
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .test import COMMANDS, CHAT_TYPES


@dp.callback_query_handler(lambda c: c.data == 'select', state=Settings.terms)
async def set_term(callback_query: types.CallbackQuery, state: FSMContext):
    await clear(state)
    markup = await select_time_keyboard()
    markup.row(InlineKeyboardButton('Назад', callback_data='back'))
    markup.insert(InlineKeyboardButton('Завершить', callback_data='done'))
    await update_last(state,
                      await bot.send_message(callback_query.message.chat.id, "Изменить время обновления", reply_markup=markup))
