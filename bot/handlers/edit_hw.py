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

COMMANDS = [
    "edit_hw",
    "edit_homework"
]


@dp.message_handler(commands=COMMANDS,  is_chat_admin=True)
@dp.message_handler(filters.Text(startswith=ALIAS),  is_chat_admin=True)
async def edit_hw(message):
    if message.text == "регулярОчка":
        return await message.reply("все сразу, круто")
    else:
        await GetHomework.subject.set()
        state = dp.get_current().current_state()
        await state.update_data(page=1)
        markup = await subjects_keyboard(['peepeepoopoo', 'poopoo'], 0)
        return await message.reply("Выберите предмет или введите его:", reply_markup=markup)


@dp.message_handler(state=GetHomework.subject)
async def edit_subject(message, state: FSMContext):
    hw_subj = message.text
    await state.update_data(subject=hw_subj)
    await GetHomework.next()
    return await message.reply("Введите название работы:")


@dp.callback_query_handler(lambda c: c.data == 'next', state=GetHomework.subject)
async def callback_edit_subject(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        await state.update_data(page=data['page'] + 1)
        page = data['page']
    markup = await subjects_keyboard(['peepeepoopoo', 'poopoo'], page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, markup)


@dp.callback_query_handler(lambda c: c.data == 'back', state=GetHomework.subject)
async def callback_edit_subject(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        await state.update_data(page=data['page'] -1)
        page = data['page']
    markup = await subjects_keyboard(['peepeepoopoo', 'poopoo'], page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, markup)


@dp.callback_query_handler(lambda c: c.data is not None, state=GetHomework.subject)
async def callback_select_subject(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await GetHomework.next()
    await bot.send_message(callback_query.message.chat.id, "Введите название работы:")


@dp.message_handler(state=GetHomework.name)
async def edit_name(message, state: FSMContext):
    hw_name = message.text
    await state.update_data(name=hw_name)
    await state.finish()
    return await message.reply("Выберите что вы хотите обновить или введите данные для замены:")