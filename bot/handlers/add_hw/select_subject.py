from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.keyboards import list_keyboard
from bot.states import SetHomework
from bot.utils.methods import update_last, clear
from bot.types.MongoDB.Collections import Chat


@dp.message_handler(state=SetHomework.subject)
async def select_subject(message: types.Message, state: FSMContext):
    hw_subj = message.text

    SUBJECTS = await Chat(message.chat.id).get_field_value("subjects")
    await clear(state)


    if hw_subj in SUBJECTS:
        await state.update_data(subject=hw_subj)
        await SetHomework.next()
        await update_last(state, await bot.send_message(message.chat.id, "Введите название работы:"))
        return
    else:
        async with state.proxy() as data:
            page = data['page']
        markup = await list_keyboard(message.chat.id, 'subject', page)
        await update_last(state,
                          await bot.send_message(message.chat.id,
                              "Данные введены неверно!\n"
                              "Выберите предмет или введите его:",
                              reply_markup=markup
                          ))


"""@dp.callback_query_handler(lambda c: c.data == 'next', state=SetHomework.subject)
async def callback_next_subject(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    SUBJECTS = await Chat(callback_query.message.chat.id).get_field_value("subjects")
    async with state.proxy() as data:
        data['page'] = data['page'] + 1
        page = data['page']
    markup = await list_keyboard(callback_query.message.chat.id, 'subject', page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id,
                                        reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'back', state=SetHomework.subject)
async def callback_back_subject(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    SUBJECTS = await Chat(callback_query.message.chat.id).get_field_value("subjects")
    async with state.proxy() as data:
        data['page'] = data['page'] - 1
        page = data['page']
    markup = await list_keyboard(callback_query.message.chat.id, 'subject', page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id,
                                        reply_markup=markup)"""


@dp.callback_query_handler(lambda c: c.data is not None, state=SetHomework.subject)
async def callback_select_subject(callback_query: types.CallbackQuery, state: FSMContext):
    # await clear(state)
    await state.update_data(subject=callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await SetHomework.next()
    await update_last(state, await bot.edit_message_text("Введите название работы:", callback_query.message.chat.id,
                                                         callback_query.message.message_id))
