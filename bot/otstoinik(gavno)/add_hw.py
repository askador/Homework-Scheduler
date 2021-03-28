import datetime
from time import strptime
from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import subjects_keyboard, calendar_keyboard
from bot.utils.methods import clear, update_last, check_date, make_datetime
#from datetime import datetime, timedelta

ALIAS = [
    "добавить дз"
]

COMMANDS = [
    "add_hw",
    "add_homework"
]

TEST = [
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '10',
    '11',
    '12',
    '13'
]


@dp.message_handler(commands=COMMANDS,  is_chat_admin=True)
@dp.message_handler(filters.Text(startswith=ALIAS),  is_chat_admin=True)
async def add_hw(message: types.Message):
    try:
        arguments = message.get_args().split()
    except Exception as e:
        arguments = None

    print(arguments)
    text = "Выберите предмет или введите его:"

    if arguments is not None and len(arguments) >= 3:
        if arguments[0] in TEST and await check_date(arguments[2]):
            return await message.reply("все сразу, круто")
        else:
            text = "Введенные данные не подходят, вызываю стандартный диалог.\nВыберите предмет или введите его:"
    elif arguments is None:
        arguments = message.text.split()
        if len(arguments) > 2 and arguments[2] in TEST and await check_date(arguments[4]):
            return await message.reply("все сразу, круто")
        else:
            text = "Введенные данные не подходят, вызываю стандартный диалог.\nВыберите предмет или введите его:"

    await SetHomework.subject.set()
    state = dp.get_current().current_state()
    await state.update_data(page=1)

    markup = await subjects_keyboard(TEST, 1)
    await update_last(state, await message.reply(text, reply_markup=markup))


@dp.message_handler(state=SetHomework.subject)
async def select_subject(message: types.Message, state: FSMContext):
    hw_subj = message.text
    await clear(state)

    if hw_subj in TEST:
        await state.update_data(subject=hw_subj)
        await SetHomework.next()
        sent = await message.reply("Введите название работы:")
        await state.update_data(last_message_id=sent.message_id)
        await state.update_data(subject=hw_subj)
        return
    else:
        async with state.proxy() as data:
            page = data['page']
        markup = await subjects_keyboard(TEST, page)
        await update_last(state, await message.reply("Данные введены неверно!\nВыберите предмет или введите его:",reply_markup=markup))


@dp.callback_query_handler(lambda c: c.data == 'next', state=SetHomework.subject)
async def callback_next_subject(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    async with state.proxy() as data:
        data['page'] = data['page'] + 1
        page = data['page']
    markup = await subjects_keyboard(TEST, page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'back', state=SetHomework.subject)
async def callback_back_subject(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    async with state.proxy() as data:
        data['page']=data['page']-1
        page = data['page']
    markup = await subjects_keyboard(TEST, page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data is not None, state=SetHomework.subject)
async def callback_select_subject(callback_query: types.CallbackQuery, state: FSMContext):
    await clear(state)
    await state.update_data(subject=callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await SetHomework.next()
    await update_last(state,  await bot.send_message(callback_query.message.chat.id, "Введите название работы:"))


@dp.message_handler(state=SetHomework.name)
async def select_name(message: types.Message, state: FSMContext):
    hw_name = message.text

    await clear(state)

    await state.update_data(name=hw_name, month=0)
    await SetHomework.next()
    markup = await calendar_keyboard(0)
    await update_last(state, await message.reply("Введите срок сдачи в формате ДД/ММ:", reply_markup=markup))


@dp.message_handler(state=SetHomework.deadline)
async def select_deadline(message: types.Message, state: FSMContext):
    await clear(state)
    hw_date = message.text.split()

    if await check_date(hw_date):
        date = await make_datetime(hw_date)
        await state.update_data(deadline=date)
        await SetHomework.next()
        text = "Введите описание работы:"
    else:
        text = "Данные введены неверно!\nВведите дату повторно:"
    await update_last(state, await message.reply(text))


@dp.callback_query_handler(lambda c: c.data == 'next_month', state=SetHomework.deadline)
async def calendar_next_month(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['month'] = data['month'] + 1
        m = data['month']

    markup = await calendar_keyboard(m)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'prev_month', state=SetHomework.deadline)
async def calendar_prev_month(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['month'] = data['month'] - 1
        m = data['month']

    markup = await calendar_keyboard(m)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'next_year', state=SetHomework.deadline)
async def calendar_next_year(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['month'] = data['month'] + 12
        m = data['month']

    markup = await calendar_keyboard(m)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'prev_year', state=SetHomework.deadline)
async def calendar_prev_year(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['month'] = data['month'] - 12
        m = data['month']

    markup = await calendar_keyboard(m)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: len(c.data.split()) > 1, state=SetHomework.deadline)
async def calendar_select_date(callback_query: types.CallbackQuery, state: FSMContext):
    date = callback_query.data.split()

    if datetime.datetime.strptime(date[1],'%Y-%m-%d') >= datetime.datetime.now():
        await clear(state)

        await state.update_data(deadline=datetime.datetime.strptime(date[1],'%Y-%m-%d'))
        await SetHomework.next()

        await update_last(state, await bot.send_message(callback_query.message.chat.id, "Введите описание работы:"))
    else:
        await bot.answer_callback_query(callback_query.id, text='Выбрана уже прошедшая дата')


@dp.message_handler(state=SetHomework.description)
async def select_description(message: types.Message, state: FSMContext):
    hw_description = message.text

    await clear(state)

    await state.update_data(description=hw_description)
    async with state.proxy() as data:
        await message.reply("Задание успешно добавлено!\n"
                                   "Предмет: {}\n"
                                   "Название: {}\n"
                                   "Срок сдачи: {}\n"
                                   "Описание: {}\n".format(data['subject'], data['name'], data['deadline'], data['description']))

    await state.finish()