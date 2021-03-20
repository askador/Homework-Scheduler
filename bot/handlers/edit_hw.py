from bot.loader import dp, bot
from aiogram.dispatcher import filters, FSMContext
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import subjects_keyboard, edit_hw_keyboard
from bot.tests.tests_bot.states_test.states_test import GetHomework
from bot.utils.methods import clear, update_last, check_date, make_datetime
from time import strptime

ALIAS = [
    "изменить дз",
    "обновить дз"
]

COMMANDS = [
    "edit_hw",
    "edit_homework"
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
async def edit_hw(message):
    try:
        arguments = message.get_args().split()
    except Exception as e:
        arguments = None

    print(arguments)
    text = "Выберите предмет или введите его:"

    if arguments is not None and len(arguments) >= 2:
        if arguments[0] in TEST:
            return await message.reply("все сразу, круто")
        else:
            text = "Введенные данные не подходят, вызываю стандартный диалог.\nВыберите предмет или введите его:"
    elif arguments is None:
        arguments = message.text.split()
        if len(arguments) > 2 and arguments[2] in TEST:
            return await message.reply("все сразу, круто")
        else:
            text = "Введенные данные не подходят, вызываю стандартный диалог.\nВыберите предмет или введите его:"

    await GetHomework.subject.set()
    state = dp.get_current().current_state()
    await state.update_data(page=1)
    markup = await subjects_keyboard(TEST, 1)
    await update_last(state, await message.reply(text, reply_markup=markup))


@dp.message_handler(state=GetHomework.subject)
async def edit_subject(message, state: FSMContext):
    hw_subj = message.text

    await clear(state)

    markup = None
    if hw_subj in TEST:
        await state.update_data(subject=hw_subj)
        await GetHomework.next()
        text = "Введите название работы:"
    else:
        text = "Данные введены неверно!\nВыберите предмет или введите его:"
        markup = await subjects_keyboard(TEST, 1)
    await update_last(state, await message.reply(text, reply_markup=markup))


@dp.callback_query_handler(lambda c: c.data == 'next', state=GetHomework.subject)
async def callback_edit_subject(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    page = 0
    async with state.proxy() as data:
        data['page'] = data['page'] + 1
        page = data['page']
    markup = await subjects_keyboard(TEST, page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'back', state=GetHomework.subject)
async def callback_edit_subject(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    page = 0
    async with state.proxy() as data:
        data['page'] = data['page'] - 1
        page = data['page']
    markup = await subjects_keyboard(TEST, page)
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data is not None, state=GetHomework.subject)
async def callback_select_subject(callback_query: types.CallbackQuery, state: FSMContext):

    await clear(state)
    await state.update_data(subject=callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await GetHomework.next()
    await update_last(state, await bot.send_message(callback_query.message.chat.id, "Введите название работы:"))


@dp.message_handler(state=GetHomework.name)
async def edit_name(message, state: FSMContext):
    hw_name = message.text

    await clear(state)

    await state.update_data(name=hw_name)
    await GetHomework.next()
    markup = await edit_hw_keyboard()
    await update_last(state, await message.reply("Выберите что вы хотите обновить или введите данные для замены:", reply_markup=markup))


@dp.callback_query_handler(lambda c: c.data is not None, state=GetHomework.choice)
async def edit_deadline(callback_query: types.CallbackQuery, state: FSMContext):

    await clear(state)

    if callback_query.data == 'deadline':
        text = "Установите новый срок сдачи:"
        await GetHomework.deadline.set()
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
    await update_last(state, await bot.send_message(callback_query.message.chat.id, text))


@dp.message_handler(state=GetHomework.choice)
async def choice_dialogue(message, state: FSMContext):
    await clear(state)

    if message.text.lower() == 'Срок сдачи':
        text = "Установите новый срок сдачи:"
        await GetHomework.deadline.set()
    elif message.text.lower() == 'Описание':
        text = "Введите новое описание:"
        await GetHomework.description.set()
    elif message.text.lower() == 'Удалить':
        text = "Задание успешно удалено"
        await state.finish()
    await update_last(state, await message.reply(text))


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


@dp.message_handler(state=GetHomework.description)
async def edit_deadline(message, state: FSMContext):
    await clear(state)
    await state.update_data(description=message.text)
    markup = await edit_hw_keyboard()
    await update_last(state, await message.reply("Описание успешно изменено!", reply_markup=markup))
    await GetHomework.choice.set()



