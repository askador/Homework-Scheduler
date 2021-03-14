from bot.loader import dp, bot
from aiogram.dispatcher import filters
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import subjects_keyboard
from bot.tests.tests_bot.states_test.states_test import Homework

ALIAS = [
    "изменить дз",
    "обновить дз"
]

@dp.message_handler(filters.Text(startswith=ALIAS), is_chat_admin=True)
async def edit_hw(message):
    if (message.text == "регулярОчка"):
        return await message.reply("все сразу, круто")
    else:
        await Homework.subject.set()
        markup = await subjects_keyboard(['peepeepoopoo', 'poopoo'])
        return await message.reply("Выберите предмет или введите его:", reply_markup=markup)


@dp.message_handler(state=Homework.subject)
async def select_subject(message):
    await Homework.next()
    return await message.reply("Введите название работы:")


@dp.callback_query_handler(func=lambda c: c.data == '0', state=Homework.subject)
async def callback_subject(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите название работы:")


@dp.message_handler(state=Homework.name)
async def find_subject(message):
    await Homework.finish()
    return await message.reply("Введите срок сдачи:")