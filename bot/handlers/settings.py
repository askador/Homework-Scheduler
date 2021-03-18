from bot.loader import dp, bot
from aiogram.dispatcher import filters, FSMContext
from aiogram import types
from bot.keyboards import settings_keyboard, settings_keyboard_subjects, settings_keyboard_subgroups, settings_keyboard_notifications, settings_keyboard_terms
from bot.tests.tests_bot.states_test.states_test import Settings
from bot.utils.methods import clear, update_last
from aiogram.types import InlineKeyboardMarkup

ALIAS = [
    "настройки"
]


COMMANDS = [
    "settings",
    "chat_settings"
]


CHAT_TYPES = [
    types.ChatType.GROUP,
    types.ChatType.SUPERGROUP
]


@dp.message_handler(commands=COMMANDS,  is_chat_admin=True)
@dp.message_handler(filters.Text(startswith=ALIAS),  is_chat_admin=True)
async def settings(message):
    markup = await settings_keyboard()
    await Settings.choice.set()
    state = dp.get_current().current_state()
    await update_last(state, await message.reply("Открыто меню настроек", reply_markup=markup))


@dp.callback_query_handler(state=Settings.choice)
async def callback_select_setting(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    await clear(state)

    markup = markup = InlineKeyboardMarkup()

    if callback_query.data == '0':
        markup = await settings_keyboard_subjects()
    elif callback_query.data == '1':
        markup = await settings_keyboard_subgroups()
    elif callback_query.data == '2':
        markup = await settings_keyboard_notifications()
    elif callback_query.data == '3':
        markup = await settings_keyboard_terms()
    elif callback_query.data == '4':
        await state.finish()
    await update_last(state, await bot.send_message(callback_query.message.chat.id, "Довай ностраивай:", reply_markup=markup))


@dp.callback_query_handler(state='*')
async def callback_finish(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.message.chat.id, "Пон")
    await state.finish()

