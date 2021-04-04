from bot.types.MongoDB.Collections import Chat
from bot.keyboards import list_keyboard
from aiogram.dispatcher import filters, FSMContext
from aiogram import types
from bot.loader import dp, bot
from bot.states import SetHomework, GetHomework


async def callback_next(callback_query: types.CallbackQuery, state: FSMContext, text):
    await bot.answer_callback_query(callback_query.id)

    async with state.proxy() as data:
        data['page'] = data['page'] + 1
        page = data['page']
    markup = await list_keyboard(callback_query.message.chat.id, text, page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


async def callback_back(callback_query: types.CallbackQuery, state: FSMContext, text):
    await bot.answer_callback_query(callback_query.id)

    async with state.proxy() as data:
        data['page'] = data['page']-1
        page = data['page']
    markup = await list_keyboard(callback_query.message.chat.id, text, page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'next', state=[SetHomework.subgroup, GetHomework.subgroup])
async def subgroup_next(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_next(callback_query, state, 'subgroup')


@dp.callback_query_handler(lambda c: c.data == 'back', state=[SetHomework.subgroup, GetHomework.subgroup])
async def subgroup_back(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_back(callback_query, state, 'subgroup')


@dp.callback_query_handler(lambda c: c.data == 'next', state=[SetHomework.subject, GetHomework.subject])
async def subject_next(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_next(callback_query, state, 'subject')


@dp.callback_query_handler(lambda c: c.data == 'back', state=[SetHomework.subject, GetHomework.subject])
async def subject_back(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_back(callback_query, state, 'subject')
