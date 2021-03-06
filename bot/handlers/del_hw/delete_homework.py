from bot.states import DeleteHomework
from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.keyboards import list_keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.types.MongoDB import Chat


@dp.callback_query_handler(lambda c: c.data == 'back', state=DeleteHomework.homework)
async def back_to_list(callback_query: types.CallbackQuery, state: FSMContext):

    await state.update_data(page=1)
    chat = Chat(callback_query.message.chat.id)
    hws = sorted(await chat.get_homeworks(filters=[{}], full_info=False), key=lambda x: x["_id"]["_id"])
    kb = await list_keyboard(callback_query.message.chat.id, 'homework', page=1, arr=hws)
    await bot.edit_message_text("Выберите задание которое хотите удалить", callback_query.message.chat.id, callback_query.message.message_id,
                                reply_markup=kb)


@dp.callback_query_handler(lambda c: c.data == 'delete', state=DeleteHomework.homework)
async def delete_homework(callback_query: types.CallbackQuery, state: FSMContext):

    chat = Chat(callback_query.message.chat.id)
    async with state.proxy() as data:
        await chat.delete_hw(data['hw_id'])

    await state.finish()
    await bot.edit_message_text("Задание было удалено", callback_query.message.chat.id, callback_query.message.message_id)


@dp.callback_query_handler(lambda c: c.data.isdigit(), state=DeleteHomework.homework)
async def approve_choice(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(hw_id=callback_query.data)

    # text может быть данными выбранного дз

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("⏪ Обратно к списку", callback_data='back'))
    markup.add(InlineKeyboardButton("❌ Удалить", callback_data='delete'))
    await bot.edit_message_text("Уверены что хотите удалить это задание?", callback_query.message.chat.id, callback_query.message.message_id,
                                reply_markup=markup)