import datetime
from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import subjects_keyboard, calendar_keyboard, subgroups_keyboard
from bot.states import SetHomework
from bot.utils.methods import clear, update_last, check_date, make_datetime, check_callback_date, check_precise
# from datetime import datetime, timedelta
from .test import TEST, ALIAS, COMMANDS


@dp.callback_query_handler(state=SetHomework.priority)
async def set_priority(callback_query: types.CallbackQuery, state: FSMContext):
    await clear(state)

    await state.update_data(priority=callback_query.data)

    async with state.proxy() as data:
        await bot.send_message(callback_query.message.chat.id, "Задание успешно добавлено!\n"
                                                               "Предмет: {}\n"
                                                               "Название: {}\n"
                                                               "Подгруппа: {}\n"
                                                               "Срок сдачи: {}\n"
                                                               "Описание: {}\n"
                                                               "Приоритет: {}".format(data['subject'], data['name'],
                                                                                      data['subgroup'],
                                                                                      data['deadline'],
                                                                                      data['description'],
                                                                                      data['priority']))
    await state.finish()
