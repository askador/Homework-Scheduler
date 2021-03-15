from bot.loader import dp, bot
from aiogram.dispatcher import filters, FSMContext
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import subjects_keyboard
from bot.tests.tests_bot.states_test.states_test import GetHomework

ALIAS = [
    "изменить дз",
    "обновить дз"
]


@dp.message_handler(filters.Text(startswith=ALIAS), is_chat_admin=True)
async def edit_hw(message):
    if message.text == "регулярОчка":
        return await message.reply("все сразу, круто")
    else:
        await GetHomework.subject.set()
        markup = await subjects_keyboard(['peepeepoopoo', 'poopoo'])
        return await message.reply("Выберите предмет или введите его:", reply_markup=markup)


@dp.message_handler(state=GetHomework.subject)
async def edit_subject(message, state: FSMContext):
    hw_subj = message.text
    await state.update_data(subject=hw_subj)
    await GetHomework.next()
    return await message.reply("Введите название работы:")


@dp.callback_query_handler(func=lambda c: c.data == '0', state=GetHomework.subject)
async def callback_edit_subject(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите название работы:")


@dp.message_handler(state=GetHomework.name)
async def edit_name(message, state: FSMContext):
    hw_name = message.text
    await state.update_data(name=hw_name)
    await GetHomework.finish()
    return await message.reply("Выберите что вы хотите обновить или введите данные для замены:")