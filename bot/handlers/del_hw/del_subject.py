from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from bot.states import DeleteHomework
from bot.keyboards import subjects_keyboard, subgroups_keyboard
from bot.utils.methods import update_last, clear
from bot.types.MongoDB.Collections import Chat


@dp.message_handler(state=DeleteHomework.subject)
async def delete_subject(message: types.Message, state: FSMContext):
    SUBJECTS = await Chat(message.chat.id).get_field_value("subjects")

    await clear(state)
    text = ''
    markup = None
    subj = message.text

    if subj in SUBJECTS:
        await state.update_data(subject=subj)
        text = 'Введите название работы:'
        await DeleteHomework.name.set()
    else:
        text = 'Предмет введен неверно!\nВыберите предмет задания или введите его:'
        markup = await subjects_keyboard(SUBJECTS, 1)

    await update_last(state, await message.reply(text, reply_markup=markup))


@dp.callback_query_handler(lambda c: c.data == 'next', state=DeleteHomework.subject)
async def callback_next_subject(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    SUBJECTS = await Chat(callback_query.message.chat.id).get_field_value("subjects")
    async with state.proxy() as data:
        data['page'] = data['page'] + 1
        page = data['page']
    markup = await subjects_keyboard(SUBJECTS, page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'back', state=DeleteHomework.subject)
async def callback_back_subject(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    SUBJECTS = await Chat(callback_query.message.chat.id).get_field_value("subjects")
    async with state.proxy() as data:
        data['page'] = data['page']-1
        page = data['page']
    markup = await subjects_keyboard(SUBJECTS, page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data is not None, state=DeleteHomework.subject)
async def callback_select_subject(callback_query: types.CallbackQuery, state: FSMContext):
    await clear(state)
    await state.update_data(subject=callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await DeleteHomework.next()
    await update_last(state, await bot.send_message(callback_query.message.chat.id, "Введите название работы:"))
