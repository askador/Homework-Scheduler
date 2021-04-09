from bot.keyboards import list_keyboard
from aiogram.dispatcher import FSMContext
from aiogram import types
from bot.loader import dp, bot
from bot.states import SetHomework, GetHomework, DeleteHomework, Settings


async def change_page(callback_query: types.CallbackQuery, state: FSMContext, text):
    page_shift = {
        'back': -1,
        'next': +1,
    }

    await bot.answer_callback_query(callback_query.id)

    async with state.proxy() as data:
        data['page'] = data['page'] + page_shift[callback_query.data]
        if data['page'] <= 0:
            data['page'] = 1
            page = 1
        else:
            page = data['page']
    markup = await list_keyboard(callback_query.message.chat.id, text, page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id,
                                        reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'next' or c.data == 'back', state=[SetHomework.subgroup, GetHomework.subgroup, Settings.remove_subjects])
async def subgroup_next(callback_query: types.CallbackQuery, state: FSMContext):
    await change_page(callback_query, state, 'subgroup')


@dp.callback_query_handler(lambda c: c.data == 'next' or c.data == 'back', state=[SetHomework.subject, GetHomework.subject, Settings.remove_subgroups])
async def subject_next(callback_query: types.CallbackQuery, state: FSMContext):
    await change_page(callback_query, state, 'subject')


@dp.callback_query_handler(lambda c: c.data == 'next' or c.data == 'back', state=[GetHomework.homework, DeleteHomework.homework])
async def subject_next(callback_query: types.CallbackQuery, state: FSMContext):
    await change_page(callback_query, state, 'homework')
