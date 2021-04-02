from bot.loader import dp, bot
from aiogram.dispatcher import filters, FSMContext
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import subjects_keyboard, edit_hw_keyboard, calendar_keyboard, subgroups_keyboard
from bot.states import GetHomework
from bot.utils.methods import clear, update_last, check_date, make_datetime, check_callback_date, check_precise
import datetime
from .test import COMMANDS, ALIAS


@dp.callback_query_handler(lambda c: c.data is not None, state=GetHomework.choice)
async def edit_choice(callback_query: types.CallbackQuery, state: FSMContext):

    await clear(state)

    markup = InlineKeyboardMarkup()
    if callback_query.data == 'deadline':
        text = "Установите новый срок сдачи:"
        await GetHomework.deadline.set()
        markup = await calendar_keyboard(0)
        await state.update_data(month=0)
    elif callback_query.data == 'description':
        text = "Введите новое описание:"
        await GetHomework.description.set()
    elif callback_query.data == 'delete':
        text = "Задание успешно удалено"
        await state.finish()
    else:
        text = "Успешно завершено"
        await state.finish()

    await bot.answer_callback_query(callback_query.id)
    await update_last(state, await bot.send_message(callback_query.message.chat.id, text, reply_markup=markup))


@dp.message_handler(state=GetHomework.choice)
async def choice_dialogue(message, state: FSMContext):
    await clear(state)

    if message.text.lower() == 'Срок сдачи':
        text = "Установите новый срок сдачи:"
        await GetHomework.deadline.set()
        markup = await calendar_keyboard(0)
        await state.update_data(month=0)
    elif message.text.lower() == 'Описание':
        text = "Введите новое описание:"
        await GetHomework.description.set()
        markup = InlineKeyboardMarkup()
    elif message.text.lower() == 'Удалить':
        text = "Задание успешно удалено"
        await state.finish()
        markup = InlineKeyboardMarkup()
    await update_last(state, await message.reply(text, reply_markup=markup))
