import datetime
from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import subjects_keyboard, calendar_keyboard, subgroups_keyboard
from bot.states import SetHomework
from bot.utils.methods import clear, update_last, check_date, make_datetime, check_callback_date, check_precise
# from datetime import datetime, timedelta
from .test import ALIAS, COMMANDS
from bot.types.MongoDB.Collections import Chat

SUBGROUPS = []


@dp.message_handler(state=SetHomework.subgroup)
async def select_subgroup(message: types.Message, state: FSMContext):
    hw_subg = message.text

    global SUBGROUPS
    SUBGROUPS = await Chat(message.chat.id).get_subgroups()
    await clear(state)

    if hw_subg in SUBGROUPS or hw_subg == 'any':
        await state.update_data(subgroup=hw_subg)
        await SetHomework.next()
        markup = await subgroups_keyboard(SUBGROUPS, 1)
        await update_last(state, await message.reply("Выберите подгруппу:", reply_markup=markup))
        return
    else:
        async with state.proxy() as data:
            page = data['page']
        markup = await subgroups_keyboard(SUBGROUPS, page)
        await update_last(state, await message.reply("Данные введены неверно!\nВыберите подгруппу или введите её:", reply_markup=markup))


@dp.callback_query_handler(lambda c: c.data == 'next', state=SetHomework.subgroup)
async def callback_next_subgroup(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    async with state.proxy() as data:
        data['page'] = data['page'] + 1
        page = data['page']
    markup = await subgroups_keyboard(SUBGROUPS, page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'back', state=SetHomework.subgroup)
async def callback_back_subgroup(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    async with state.proxy() as data:
        data['page'] = data['page']-1
        page = data['page']
    markup = await subgroups_keyboard(SUBGROUPS, page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data is not None, state=SetHomework.subgroup)
async def callback_select_subgroup(callback_query: types.CallbackQuery, state: FSMContext):
    await clear(state)
    await state.update_data(subgroup=callback_query.data, page=0)
    await bot.answer_callback_query(callback_query.id)
    await SetHomework.next()
    markup = await calendar_keyboard(0)
    await update_last(state, await bot.send_message(callback_query.message.chat.id, "Введите срок сдачи в формате ДД/ММ:", reply_markup=markup))
