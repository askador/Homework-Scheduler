from bot.loader import dp, bot
from aiogram.dispatcher import filters, FSMContext
from aiogram import types
from bot.keyboards import select_time_keyboard, settings_keyboard_appearance, settings_keyboard_moderators, settings_keyboard, settings_keyboard_subjects, settings_keyboard_subgroups, settings_keyboard_notifications, settings_keyboard_terms
from bot.tests.tests_bot.states_test.states_test import Settings
from bot.utils.methods import clear, update_last
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .test import COMMANDS, CHAT_TYPES


@dp.callback_query_handler(state=Settings.choice)
async def callback_select_setting(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    await clear(state)

    markup = InlineKeyboardMarkup()
    text = 'Sample text'

    if callback_query.data == '0':
        await Settings.subjects.set()
        markup = await settings_keyboard_subjects()
    elif callback_query.data == '1':
        await Settings.subgroups.set()
        markup = await settings_keyboard_subgroups()
    elif callback_query.data == '2':
        await Settings.notifications.set()
        markup = await settings_keyboard_notifications()
    elif callback_query.data == '3':
        await Settings.terms.set()
        markup = await settings_keyboard_terms()
    elif callback_query.data == '4':
        await Settings.moderators.set()
        markup = await settings_keyboard_moderators()
    elif callback_query.data == '5':
        await Settings.appearance.set()
        markup = await settings_keyboard_appearance()
    elif callback_query.data == '6':
        await state.finish()
        text = 'Настройка завершена'
    await update_last(state, await bot.send_message(callback_query.message.chat.id, text, reply_markup=markup))
