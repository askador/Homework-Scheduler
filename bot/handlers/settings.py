from bot.loader import dp, bot
from aiogram.dispatcher import filters, FSMContext
from aiogram import types
from bot.keyboards import settings_keyboard
from bot.tests.tests_bot.states_test.states_test import Settings

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
    return await message.reply("Себя настрой лучше", reply_markup=markup)


@dp.callback_query_handler(state=Settings.choice)
async def callback_select_subject(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    if callback_query.id == 'Subjects':
        await bot.send_message(callback_query.message.chat.id, "Довай ностраивай:")
    elif callback_query.id == 'Subgroups':
        await bot.send_message(callback_query.message.chat.id, "Довай ностраивай:")