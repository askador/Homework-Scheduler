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

COMMANDS = [
    "add_hw",
    "add_homework"
]


@dp.message_handler(commands=COMMANDS,  is_chat_admin=True)
@dp.message_handler(filters.Text(startswith=ALIAS),  is_chat_admin=True)
async def add_hw(message):
    if message.text == "регулярОчка":
        return await message.reply("все сразу, круто")
    else:
        await SetHomework.subject.set()
        state = dp.get_current().current_state()
        await state.update_data(page=1)
        markup = await subjects_keyboard(['peepeepoopoo', 'poopoo'], 1)
        return await message.reply("Выберите предмет или введите его:", reply_markup=markup)


@dp.message_handler(state=SetHomework.subject)
async def select_subject(message: types.Message, state: FSMContext):
    hw_subj = message.text
    await state.update_data(subject=hw_subj)
    await SetHomework.next()
    return await message.reply("Введите название работы:")


@dp.callback_query_handler(lambda c: c.data == 'next', state=SetHomework.subject)
async def callback_next_subject(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        await state.update_data(page=data['page'] + 1)
        page = data['page']
    markup = await subjects_keyboard(['peepeepoopoo', 'poopoo'], page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, markup)


@dp.callback_query_handler(lambda c: c.data == 'back', state=SetHomework.subject)
async def callback_back_subject(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        await state.update_data(page=data['page']-1)
        page = data['page']
    markup = await subjects_keyboard(['peepeepoopoo', 'poopoo'], page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, markup)


@dp.callback_query_handler(lambda c: c.data is not None, state=SetHomework.subject)
async def callback_select_subject(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await SetHomework.next()
    await bot.send_message(callback_query.message.chat.id, "Введите название работы:")


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
    await state.finish()
    return await message.reply("Задание успешно добавлено!")