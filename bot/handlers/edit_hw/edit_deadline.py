from bot.loader import dp, bot
from aiogram.dispatcher import filters, FSMContext
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import subjects_keyboard, edit_hw_keyboard, calendar_keyboard, subgroups_keyboard
from bot.states import GetHomework
from bot.types.MongoDB import Chat
from bot.utils.methods import clear, update_last, check_date, make_datetime, check_callback_date, check_precise
import datetime


@dp.message_handler(state=GetHomework.deadline)
async def edit_deadline(message, state: FSMContext):
    hw_date = message.text
    await clear(state)

    if await check_date(hw_date):
        date = await make_datetime(hw_date)
        await state.update_data(deadline=date)
        text = "Срок сдачи успешно изменен!"
        await GetHomework.choice.set()
        markup = await edit_hw_keyboard()
        await update_last(state, await message.reply(text, reply_markup=markup))
    else:
        text = "Данные введены неверно!\nВведите дату повторно:"
        await update_last(state, await message.reply(text))


@dp.callback_query_handler(lambda c: c.data == 'next_month', state=GetHomework.deadline)
async def calendar_next_month(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['month'] = data['month'] + 1
        m = data['month']

    markup = await calendar_keyboard(m)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'prev_month', state=GetHomework.deadline)
async def calendar_prev_month(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['month'] = data['month'] - 1
        m = data['month']

    markup = await calendar_keyboard(m)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'next_year', state=GetHomework.deadline)
async def calendar_next_year(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['month'] = data['month'] + 12
        m = data['month']

    markup = await calendar_keyboard(m)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'prev_year', state=GetHomework.deadline)
async def calendar_prev_year(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['month'] = data['month'] - 12
        m = data['month']

    markup = await calendar_keyboard(m)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: len(c.data.split()) > 1, state=GetHomework.deadline)
async def calendar_select_date(callback_query: types.CallbackQuery, state: FSMContext):
    date = callback_query.data.split()

    if await check_callback_date(datetime.datetime.strptime(date[1], '%Y-%m-%d')):
        await clear(state)

        await state.update_data(deadline=datetime.datetime.strptime(date[1], '%Y-%m-%d'))
        await GetHomework.next()

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('Дальше', callback_data='next'))
        await state.update_data(noskip=0)
        await update_last(state, await bot.send_message(callback_query.message.chat.id, "Введите время в "
                                                                                        "формате HH:MM или нажмите "
                                                                                        "дальше чтобы добавить с "
                                                                                        "временем по умолчанию:",
                                                        reply_markup=markup))
    else:
        await bot.answer_callback_query(callback_query.id, text='Выбрана уже прошедшая дата')


@dp.message_handler(state=GetHomework.deadline_precise)
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
        await GetHomework.choice.set()

        text = "Выберите что вы хотите отредактировать: "
        markup = await edit_hw_keyboard()
    else:
        text = "Данные введены неверно!\nВведите время повторно:"
        markup = InlineKeyboardMarkup()

        if noskip != 1:
            markup.add(InlineKeyboardButton('Дальше', callback_data='next'))

    await update_last(state, await message.reply(text, reply_markup=markup))


@dp.callback_query_handler(lambda c: c.data == 'next', state=GetHomework.deadline_precise)
async def skip_precise(callback_query: types.CallbackQuery, state: FSMContext):

    await clear(state)

    async with state.proxy() as data:
        date = data['deadline']

    if await check_precise(date, '00:00'):
        time = datetime.datetime.strptime('00:00', '%H:%M')
        date = date.replace(hour=time.hour)
        date = date.replace(minute=time.minute)

        await state.update_data(deadline=date)

        chat = Chat(callback_query.message.chat.id)
        async with state.proxy() as data:
            print(data['hw_id'], data['deadline'])
            await chat.update_hw(_id=int(data['hw_id']), deadline=data['deadline'])

        await GetHomework.choice.set()

        text = "Выберите что вы хотите отредактировать: "
        markup = await edit_hw_keyboard()
    else:
        await state.update_data(noskip=1)
        text = "Данные введены неверно!\nВведите время повторно:"
        markup = None
    await update_last(state, await bot.send_message(callback_query.message.chat.id, text, reply_markup=markup))