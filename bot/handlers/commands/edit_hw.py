from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher import filters
from aiogram.dispatcher import FSMContext
from bot.loader import dp
from bot.keyboards import list_keyboard
from bot.states import GetHomework
from bot.data.commands.edit_hw import COMMANDS, COMMANDS_TEXT
from bot.types.MongoDB.Collections import Chat
from bot.utils.methods import bind_student_to_chat, update_last


@dp.message_handler(Command(commands=COMMANDS_TEXT, prefixes="!"), access_level='moderator')
@dp.message_handler(commands=COMMANDS, access_level='moderator')
async def edit_hw(message, state: FSMContext):
    await bind_student_to_chat(message.from_user.id, message.chat.id)

    chat_id = message.chat.id
    chat = Chat(chat_id)

    await GetHomework.homework.set()
    state = dp.get_current().current_state()
    await state.update_data(page=1)

    args = message.get_args().split() if message.is_command() else message.text.split()[1:]

    homeworks = sorted(await chat.homeworks_search(args=args, full_info=False), key=lambda x: x["_id"]["_id"])

    if not homeworks:
        await message.reply("По запросу ничего не нашлось")
        return

    kb = await list_keyboard(message.chat.id, 'homework', page=1, arr=homeworks)
    await update_last(state,
                      await message.answer(text="Выберите задание, которое Вы хотите редактировать",
                                           reply_markup=kb))
