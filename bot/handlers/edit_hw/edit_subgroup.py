from bot.loader import dp, bot
from aiogram.dispatcher import filters, FSMContext
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import subjects_keyboard, edit_hw_keyboard, calendar_keyboard, subgroups_keyboard
from bot.states import GetHomework
from bot.utils.methods import clear, update_last, check_date, make_datetime, check_callback_date, check_precise
import datetime
from bot.types.MongoDB.Collections import Chat


@dp.message_handler(state=GetHomework.subgroup)
async def edit_subgroup(message, state: FSMContext):
    SUBGROUPS = await Chat(message.chat.id).get_field_value("subgroups")
    hw_subg = message.text

    await clear(state)

    markup = None
    if hw_subg in SUBGROUPS:
        await state.update_data(subgroup=hw_subg)
        await GetHomework.next()
        markup = await edit_hw_keyboard()
        text = "Выберите что вы хотите отредактировать:"
    else:
        text = "Данные введены неверно!\nВыберите подгруппу или введите её:"
        markup = await subgroups_keyboard(SUBGROUPS, 1)
    await update_last(state, await message.reply(text, reply_markup=markup))


@dp.callback_query_handler(lambda c: c.data == 'next', state=GetHomework.subgroup)
async def callback_edit_subgroup(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    SUBGROUPS = await Chat(callback_query.message.chat.id).get_field_value("subgroups")
    async with state.proxy() as data:
        data['page'] = data['page'] + 1
        page = data['page']
    markup = await subgroups_keyboard(SUBGROUPS, page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'back', state=GetHomework.subgroup)
async def callback_edit_subgroup(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    SUBGROUPS = await Chat(callback_query.message.chat.id).get_field_value("subgroups")
    async with state.proxy() as data:
        data['page'] = data['page'] - 1
        page = data['page']
    markup = await subgroups_keyboard(SUBGROUPS, page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data is not None, state=GetHomework.subgroup)
async def callback_select_subgroup(callback_query: types.CallbackQuery, state: FSMContext):

    await clear(state)
    await state.update_data(subgroup=callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await GetHomework.next()
    markup = await edit_hw_keyboard()
    await update_last(state, await bot.send_message(callback_query.message.chat.id, "Выберите что вы хотите отредактировать:", reply_markup=markup))
