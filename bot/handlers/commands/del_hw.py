from bot.loader import dp
from aiogram import types
from aiogram.dispatcher import filters
from bot.states import DeleteHomework
from bot.keyboards import list_keyboard
from bot.data.commands.del_hw import COMMANDS, ALIAS
from bot.types.MongoDB.Collections import Chat


@dp.message_handler(filters.Text(startswith=ALIAS), access_level='moderator')
@dp.message_handler(commands=COMMANDS,  access_level='moderator')
async def del_hw(message: types.Message):
    chat_id = message.chat.id

    chat = Chat(chat_id)

    # homeworks = await chat.get_homeworks(filters=[{}], full_info=False)

    await DeleteHomework.homework.set()
    state = dp.get_current().current_state()
    await state.update_data(page=1)

    kb = await list_keyboard(message.chat.id, 'homework', 1)
    await message.answer(text="Выберите задание, которое Вы хотите удалить",
                         reply_markup=kb)