from bot.loader import dp, bot
from bot.scheduler import scheduler
from aiogram.dispatcher import FSMContext
from aiogram import types
from bot.states import AddChat
from bot.types.MongoDB.Collections import Chat


@dp.callback_query_handler(state=AddChat.subgroups)
async def no_subgroups(callback_query: types.CallbackQuery, state: FSMContext):
    filtered_subgroups = []
    async with state.proxy() as data:
        data['chat_subgroups'] = filtered_subgroups

    async with state.proxy() as data:
        chat_id = data['chat_id']
        chat_title = data['chat_title']
        chat_admins = data['chat_admins']
        chat_subjects = data['chat_subjects']
        chat_subgroups = data['chat_subgroups']

    chat_id = callback_query.message.chat.id
    chat = Chat(chat_id)
    await chat.add(title=chat_title,
                   admins=chat_admins,
                   subjects=chat_subjects,
                   subgroups=chat_subgroups,
                   students=chat_admins)

    await state.finish()

    await bot.send_message(chat.id, "Вы успешно настроили бота!\n\n"
                           "Чтобы узнать подробнее про возможности Homework Scheduler, введите /help")


@dp.message_handler(state=AddChat.subgroups)
async def process_subgroups(message, state):

    subgroups = message.text.split(',')
    filtered_subgroups = []

    for subgroup in subgroups:
        if subgroup.strip() != '':
            filtered_subgroups.append(subgroup.strip())

    async with state.proxy() as data:
        data['chat_subgroups'] = filtered_subgroups

    async with state.proxy() as data:
        chat_id = data['chat_id']
        chat_title = data['chat_title']
        chat_admins = data['chat_admins']
        chat_subjects = data['chat_subjects']
        chat_subgroups = data['chat_subgroups']

    chat_id = message.chat.id
    chat = Chat(chat_id)
    await chat.add(title=chat_title,
                   admins=chat_admins,
                   subjects=chat_subjects,
                   subgroups=chat_subgroups,
                   students=chat_admins)

    await state.finish()

    await message.answer("Вы успешно настроили бота!\n\n"
                         "Чтобы узнать подробнее про возможности Homework Scheduler, введите /help")
    # scheduler.add_job(show_hw, 'cron', hour=15, minute=19, args={message}) добавить в список определенного времени