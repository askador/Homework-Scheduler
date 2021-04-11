from bot.keyboards import list_keyboard
from aiogram.dispatcher import FSMContext
from aiogram import types
from bot.loader import dp, bot
from bot.states import SetHomework, GetHomework, DeleteHomework, Settings, ShowHw
from aiogram.types import InlineKeyboardButton


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
            if text == 'special':
                markup = await list_keyboard(callback_query.message.chat.id, text, page, data['special'])
                if len(data['to_display']) != 0:
                    markup.add(InlineKeyboardButton('⏪ Отменить', callback_data='redo'))
                markup.add(InlineKeyboardButton('Сохранить изменения', callback_data='save'))
            else:
                markup = await list_keyboard(callback_query.message.chat.id, text, page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id,
                                        reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'next' or c.data == 'back', state=[SetHomework.subgroup, GetHomework.subgroup])
async def subgroup_next(callback_query: types.CallbackQuery, state: FSMContext):
    await change_page(callback_query, state, 'subgroup')


@dp.callback_query_handler(lambda c: c.data == 'next' or c.data == 'back', state=[SetHomework.subject, GetHomework.subject])
async def subject_next(callback_query: types.CallbackQuery, state: FSMContext):
    await change_page(callback_query, state, 'subject')


@dp.callback_query_handler(lambda c: c.data == 'next' or c.data == 'back',
                           state=[GetHomework.homework, DeleteHomework.homework, ShowHw.week])
async def subject_next(callback_query: types.CallbackQuery, state: FSMContext):
    await change_page(callback_query, state, 'homework')


@dp.callback_query_handler(lambda c: c.data == 'next' or c.data == 'back', state=[Settings.remove_subjects, Settings.remove_subgroups])
async def subject_next(callback_query: types.CallbackQuery, state: FSMContext):
    await change_page(callback_query, state, 'special')