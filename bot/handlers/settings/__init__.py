from .settings_subject import subject_add, subject_remove
from .settings_subgroup import subgroup_edit, subgroup_add, subgroup_remove
from .settings_terms import set_term
from .settings_moderators import moderators_add, moderators_remove
from .settings_choice import callback_select_setting

from bot.loader import dp, bot
from aiogram.dispatcher import filters, FSMContext
from aiogram import types
from bot.keyboards import select_time_keyboard, settings_keyboard_appearance, settings_keyboard_moderators, settings_keyboard, settings_keyboard_subjects, settings_keyboard_subgroups, settings_keyboard_notifications, settings_keyboard_terms
from bot.tests.tests_bot.states_test.states_test import Settings
from bot.utils.methods import clear, update_last
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .test import COMMANDS, CHAT_TYPES


@dp.message_handler(commands=COMMANDS,  is_chat_admin=True)
@dp.message_handler(filters.Text(startswith=ALIAS),  is_chat_admin=True)
async def settings(message):
    markup = await settings_keyboard()
    await Settings.choice.set()
    state = dp.get_current().current_state()
    await update_last(state, await message.reply("Открыто меню настроек", reply_markup=markup))


@dp.callback_query_handler(lambda c: c.data == 'back', state='*')
async def back_to_choice(callback_query: types.CallbackQuery, state: FSMContext):
    await clear(state)
    await Settings.choice.set()
    markup = await settings_keyboard()
    await update_last(state, await bot.send_message(callback_query.message.chat.id,"Меню настроек", reply_markup=markup))


@dp.callback_query_handler(lambda c: c.data == 'done', state='*')
async def back_to_choice(callback_query: types.CallbackQuery, state: FSMContext):
    await clear(state)
    await state.finish()
    await bot.send_message(callback_query.message.chat.id, "Настройка завершена")