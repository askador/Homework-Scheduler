from bot.loader import dp, bot
from aiogram.dispatcher import filters, FSMContext
from aiogram import types
from bot.keyboards import settings_keyboard
from bot.tests.tests_bot.states_test.states_test import Settings

ALIAS = [
    "настройки"
]


CHAT_TYPES = [
    types.ChatType.GROUP,
    types.ChatType.SUPERGROUP
]


@dp.message_handler(filters.Text(equals=ALIAS), filters.ChatTypeFilter(CHAT_TYPES))
async def settings(message):
    markup = await settings_keyboard()
    await Settings.choice.set()
    return await message.reply("Себя настрой лучше", reply_markup=markup)


@dp.callback_query_handler(state=Settings.choice)
async def callback_select_subject(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    if callback_query.id == 'Subjects':
        await bot.send_message(callback_query.from_user.id, "Довай ностраивай:")
    elif callback_query.id == 'Subgroups':
        await bot.send_message(callback_query.from_user.id, "Довай ностраивай:")