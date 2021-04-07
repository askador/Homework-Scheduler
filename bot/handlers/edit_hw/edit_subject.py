from bot.loader import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram import types
from bot.keyboards import subjects_keyboard
from bot.states import GetHomework
from bot.utils.methods import clear, update_last
from bot.types.MongoDB.Collections import Chat


@dp.message_handler(state=GetHomework.subject)
async def edit_subject(message, state: FSMContext):
    SUBJECTS = await Chat(message.chat.id).get_field_value("subjects")
    hw_subj = message.text
    text = ''

    await clear(state)

    markup = None
    if hw_subj in SUBJECTS:
        await state.update_data(subject=hw_subj)
        await GetHomework.next()
        text = "Введите название работы:"
    else:
        text = "Данные введены неверно!\nВыберите предмет или введите его:"
        markup = await subjects_keyboard(SUBJECTS, 1)
    await update_last(state, await message.reply(text, reply_markup=markup))


@dp.callback_query_handler(lambda c: c.data == 'next', state=GetHomework.subject)
async def callback_edit_subject(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    SUBJECTS = await Chat(callback_query.message.chat.id).get_field_value("subjects")
    async with state.proxy() as data:
        data['page'] = data['page'] + 1
        page = data['page']
    markup = await subjects_keyboard(SUBJECTS, page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'back', state=GetHomework.subject)
async def callback_edit_subject(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    SUBJECTS = await Chat(callback_query.message.chat.id).get_field_value("subjects")
    async with state.proxy() as data:
        data['page'] = data['page'] - 1
        page = data['page']
    markup = await subjects_keyboard(SUBJECTS, page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data is not None, state=GetHomework.subject)
async def callback_select_subject(callback_query: types.CallbackQuery, state: FSMContext):

    await clear(state)
    await state.update_data(subject=callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await GetHomework.next()
    await update_last(state, await bot.send_message(callback_query.message.chat.id, "Введите название работы:"))