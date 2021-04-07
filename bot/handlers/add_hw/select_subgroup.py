from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.keyboards import calendar_keyboard, list_keyboard
from bot.states import SetHomework
from bot.utils.methods import update_last
from bot.types.MongoDB.Collections import Chat


@dp.message_handler(state=SetHomework.subgroup)
async def select_subgroup(message: types.Message, state: FSMContext):
    hw_subg = message.text

    SUBGROUPS = await Chat(message.chat.id).get_field_value("subgroups")
    # await clear(state)

    if hw_subg in SUBGROUPS or hw_subg == 'any':
        if hw_subg == 'any':
            hw_subg = ''
        await state.update_data(subgroup=hw_subg)
        await SetHomework.next()
        markup = await list_keyboard(message.chat.id, 'subgroup', 1)
        await update_last(state, await bot.send_message(message.chat.id, "Выберите подгруппу:",
                                                        reply_markup=markup))
        return
    else:
        async with state.proxy() as data:
            page = data['page']
        markup = await list_keyboard(message.chat.id, 'subgroup', page)
        await update_last(state, await bot.send_message(message.chat.id,
                                                        "Данные введены неверно!\nВыберите подгруппу или введите её:",
                                                        reply_markup=markup))


"""@dp.callback_query_handler(lambda c: c.data == 'next', state=SetHomework.subgroup)
async def callback_next_subgroup(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    SUBGROUPS = await Chat(callback_query.message.chat.id).get_field_value("subgroups")
    async with state.proxy() as data:
        data['page'] = data['page'] + 1
        page = data['page']
    markup = await list_keyboard(callback_query.message.chat.id, 'subgroup', 1)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'back', state=SetHomework.subgroup)
async def callback_back_subgroup(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    SUBGROUPS = await Chat(callback_query.message.chat.id).get_field_value("subgroups")
    async with state.proxy() as data:
        data['page'] = data['page']-1
        page = data['page']
    markup = await list_keyboard(callback_query.message.chat.id, 'subgroup', 1)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)
"""


@dp.callback_query_handler(lambda c: c.data is not None, state=SetHomework.subgroup)
async def callback_select_subgroup(callback_query: types.CallbackQuery, state: FSMContext):
    # await clear(state)
    await state.update_data(subgroup=callback_query.data, page=0)
    await bot.answer_callback_query(callback_query.id)
    await SetHomework.next()
    markup = await calendar_keyboard(0)
    await update_last(state, await bot.edit_message_text("Введите срок сдачи в формате ДД/ММ:",
                                                         callback_query.message.chat.id,
                                                         callback_query.message.message_id, reply_markup=markup))
