from bot.loader import dp, bot
from aiogram.dispatcher import filters, FSMContext
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import subjects_keyboard, edit_hw_keyboard, calendar_keyboard, subgroups_keyboard
from bot.tests.tests_bot.states_test.states_test import GetHomework
from bot.utils.methods import clear, update_last, check_date, make_datetime, check_callback_date, check_precise
import datetime
from .test import TEST, COMMANDS, ALIAS


@dp.message_handler(state=GetHomework.subject)
async def edit_subject(message, state: FSMContext):
    hw_subj = message.text

    await clear(state)

    markup = None
    if hw_subj in TEST:
        await state.update_data(subject=hw_subj)
        await GetHomework.next()
        text = "Введите название работы:"
    else:
        text = "Данные введены неверно!\nВыберите предмет или введите его:"
        markup = await subjects_keyboard(TEST, 1)
    await update_last(state, await message.reply(text, reply_markup=markup))


@dp.callback_query_handler(lambda c: c.data == 'next', state=GetHomework.subject)
async def callback_edit_subject(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    async with state.proxy() as data:
        data['page'] = data['page'] + 1
        page = data['page']
    markup = await subjects_keyboard(TEST, page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'back', state=GetHomework.subject)
async def callback_edit_subject(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    async with state.proxy() as data:
        data['page'] = data['page'] - 1
        page = data['page']
    markup = await subjects_keyboard(TEST, page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data is not None, state=GetHomework.subject)
async def callback_select_subject(callback_query: types.CallbackQuery, state: FSMContext):

    await clear(state)
    await state.update_data(subject=callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await GetHomework.next()
    await update_last(state, await bot.send_message(callback_query.message.chat.id, "Введите название работы:"))