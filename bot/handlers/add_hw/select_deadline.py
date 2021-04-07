import datetime
from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import calendar_keyboard
from bot.states import SetHomework
from bot.utils.methods import clear, update_last, check_date, make_datetime, check_callback_date, check_precise


@dp.message_handler(state=SetHomework.deadline)
async def select_deadline(message: types.Message, state: FSMContext):
    # await clear(state)
    hw_date = message.text.split()

    if await check_date(hw_date):
        date = await make_datetime(hw_date)
        await state.update_data(deadline=date)
        await SetHomework.description.set()
        text = "Введите описание работы:"
    else:
        text = "Данные введены неверно!\nВведите дату повторно:"
    await update_last(state, await bot.send_message(message.chat.id, text))


@dp.callback_query_handler(lambda c: c.data == 'next_month', state=SetHomework.deadline)
async def calendar_next_month(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['month'] = data['month'] + 1
        m = data['month']

    markup = await calendar_keyboard(m)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id,
                                        reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'prev_month', state=SetHomework.deadline)
async def calendar_prev_month(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['month'] = data['month'] - 1
        m = data['month']

    markup = await calendar_keyboard(m)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id,
                                        reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'next_year', state=SetHomework.deadline)
async def calendar_next_year(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['month'] = data['month'] + 12
        m = data['month']

    markup = await calendar_keyboard(m)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id,
                                        reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'prev_year', state=SetHomework.deadline)
async def calendar_prev_year(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['month'] = data['month'] - 12
        m = data['month']

    markup = await calendar_keyboard(m)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id,
                                        reply_markup=markup)


@dp.callback_query_handler(lambda c: len(c.data.split()) > 1, state=SetHomework.deadline)
async def calendar_select_date(callback_query: types.CallbackQuery, state: FSMContext):
    # print(callback_query.data)
    date = callback_query.data.split()

    if await check_callback_date(datetime.datetime.strptime(date[1], '%Y-%m-%d')):
        # await clear(state)

        await state.update_data(deadline=datetime.datetime.strptime(date[1], '%Y-%m-%d'))
        await SetHomework.next()

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('Дальше', callback_data='next'))
        await state.update_data(noskip=0)
        await update_last(state, await bot.edit_message_text("Введите время в "
                                                             "формате HH:MM или нажмите "
                                                             "'Дальше' чтобы добавить с "
                                                             "временем по умолчанию:",
                                                             callback_query.message.chat.id,
                                                             callback_query.message.message_id,
                                                             reply_markup=markup))
    else:
        await bot.answer_callback_query(callback_query.id, text='Выбрана уже прошедшая дата')


@dp.message_handler(state=SetHomework.deadline_precise)
async def select_deadline_precise(message: types.Message, state: FSMContext):
    await clear(state)

    time = message.text
    async with state.proxy() as data:
        date = data['deadline']
        noskip = data['noskip']

    if await check_precise(date, time):
        time = datetime.datetime.strptime(time, '%H:%M')
        date = date.replace(hour=time.hour)
        date = date.replace(minute=time.minute)

        await state.update_data(deadline=date)
        await SetHomework.next()

        text = "Введите описание работы: "
        markup = InlineKeyboardMarkup()
    else:
        text = "Данные введены неверно!\nВведите время повторно:"
        markup = InlineKeyboardMarkup()

        if noskip != 1:
            markup.add(InlineKeyboardButton('Дальше', callback_data='next'))

    await update_last(state, await bot.send_message(message.chat.id, text,
                                                         reply_markup=markup))


@dp.callback_query_handler(state=SetHomework.deadline_precise)
async def skip_precise(callback_query: types.CallbackQuery, state: FSMContext):
    # await clear(state)

    async with state.proxy() as data:
        date = data['deadline']

    if await check_precise(date, '00:00'):
        await SetHomework.next()

        text = "Введите описание работы: "
    else:
        await state.update_data(noskip=1)
        text = "Данные введены неверно!\nВведите время повторно:"
    await update_last(state, await bot.edit_message_text(text, callback_query.message.chat.id,
                                                         callback_query.message.message_id))
