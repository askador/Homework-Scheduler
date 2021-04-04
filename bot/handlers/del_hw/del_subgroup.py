from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from bot.states import DeleteHomework
from bot.keyboards import subjects_keyboard, subgroups_keyboard
from bot.utils.methods import update_last, clear
from bot.types.MongoDB.Collections import Chat


@dp.message_handler(state=DeleteHomework.subgroup)
async def delete_subgroup(message: types.Message, state: FSMContext):
    SUBGROUPS = await Chat(message.chat.id).get_field_value("subgroups")

    await clear(state)
    text = ''
    markup = None
    subg = message.text

    if subg in SUBGROUPS:
        await state.update_data(subgroup=subg)
        text = 'Удаление работы'

        # TODO implement database interaction
        # hw.delete()

        await state.finish()
    else:
        text = 'Подгруппа введена неверно!\nВыберите подгруппу или введите её:'
        markup = await subjects_keyboard(SUBGROUPS, 1)

    await update_last(state, await message.reply(text, reply_markup=markup))


@dp.callback_query_handler(lambda c: c.data == 'next', state=DeleteHomework.subgroup)
async def callback_next_subgroup(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    SUBGROUPS = await Chat(callback_query.message.chat.id).get_field_value("subgroups")
    async with state.proxy() as data:
        data['page'] = data['page'] + 1
        page = data['page']
    markup = await subgroups_keyboard(SUBGROUPS, page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'back', state=DeleteHomework.subgroup)
async def callback_back_subgroup(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    SUBGROUPS = await Chat(callback_query.message.chat.id).get_field_value("subgroups")
    async with state.proxy() as data:
        data['page'] = data['page']-1
        page = data['page']
    markup = await subgroups_keyboard(SUBGROUPS, page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data is not None, state=DeleteHomework.subgroup)
async def callback_select_subgroup(callback_query: types.CallbackQuery, state: FSMContext):
    await clear(state)
    await state.update_data(subgroup=callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await state.finish()
    await update_last(state, await bot.send_message(callback_query.message.chat.id, "Удаление работы"))
