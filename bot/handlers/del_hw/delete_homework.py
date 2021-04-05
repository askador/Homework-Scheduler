from bot.states import DeleteHomework
from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from bot.keyboards import list_keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@dp.callback_query_handler(lambda c: c.data == 'back', state=DeleteHomework.homework)
async def back_to_list(callback_query: types.CallbackQuery, state: FSMContext):

    await state.update_data(page=1)
    kb = await list_keyboard(callback_query.message.chat.id, 'homework', 1)
    await bot.edit_message_text("Видалив копчене", callback_query.message.chat.id, callback_query.message.message_id,
                          reply_markup=kb)


@dp.callback_query_handler(lambda c: c.data == 'delete', state=DeleteHomework.homework)
async def delete_homework(callback_query: types.CallbackQuery, state: FSMContext):

    # TODO
    # deleting hw

    await state.finish()
    await bot.edit_message_text("Видалив копчене", callback_query.message.chat.id, callback_query.message.message_id)


@dp.callback_query_handler(lambda c: c.data is not None, state=DeleteHomework.homework)
async def approve_choice(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(id=callback_query.data)

    # text может быть данными выбранного дз

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Обратно к списку", callback_data='back'))
    markup.add(InlineKeyboardButton("Удалить", callback_data='delete'))
    await bot.edit_message_text("Чи треба видаляти копчене?", callback_query.message.chat.id, callback_query.message.message_id,
                          reply_markup=markup)