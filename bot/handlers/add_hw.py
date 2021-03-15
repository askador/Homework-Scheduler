from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import subjects_keyboard
from bot.tests.tests_bot.states_test.states_test import SetHomework
#from datetime import datetime, timedelta

ALIAS = [
    "добавить дз"
]


@dp.message_handler(filters.Text(equals=ALIAS), is_chat_admin=True)
async def add_hw(message):
    if message.text == "регулярОчка":
        return await message.reply("все сразу, круто")
    else:
        await SetHomework.subject.set()
        markup = await subjects_keyboard(['peepeepoopoo', 'poopoo'])
        return await message.reply("Выберите предмет или введите его:", reply_markup=markup)


@dp.message_handler(state=SetHomework.subject)
async def select_subject(message: types.Message, state: FSMContext):
    hw_subj = message.text
    await state.update_data(subject=hw_subj)
    await SetHomework.next()
    return await message.reply("Введите название работы:")


@dp.callback_query_handler(state=SetHomework.subject)
async def callback_select_subject(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите название работы:")


@dp.message_handler(state=SetHomework.name)
async def select_name(message: types.Message, state: FSMContext):
    hw_name = message.text
    await state.update_data(name=hw_name)
    await SetHomework.next()
    return await message.reply("Введите срок сдачи:")


@dp.message_handler(state=SetHomework.deadline)
async def select_deadline(message: types.Message, state: FSMContext):
    hw_date = message.text
    await state.update_data(deadline=hw_date)
    await SetHomework.next()
    return await message.reply("Введите описание работы:")


@dp.message_handler(state=SetHomework.description)
async def select_description(message: types.Message, state: FSMContext):
    hw_description = message.text
    await state.update_data(description=hw_description)
    await SetHomework.finish()
    return await message.reply("Задание успешно добавлено!")