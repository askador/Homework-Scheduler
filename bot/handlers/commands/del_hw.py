from bot.loader import dp
from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from bot.states import DeleteHomework
from bot.keyboards import list_keyboard
from bot.data.commands.del_hw import COMMANDS, COMMANDS_TEXT
from aiogram.dispatcher.filters import Command
from bot.types.MongoDB.Collections import Chat
from bot.utils.methods import bind_student_to_chat, update_last


@dp.message_handler(Command(commands=COMMANDS_TEXT, prefixes="!"), access_level='moderator')
@dp.message_handler(commands=COMMANDS,  access_level='moderator')
async def del_hw(message: types.Message, state: FSMContext):
    await bind_student_to_chat(message.from_user.id, message.chat.id)


    chat_id = message.chat.id
    chat = Chat(chat_id)

    await DeleteHomework.homework.set()
    state = dp.get_current().current_state()
    await state.update_data(page=1)

    args = message.get_args().split() if message.is_command() else message.text.split()[1:]

    homeworks = sorted(await chat.homeworks_search(args=args, full_info=False), key=lambda x: x["_id"]["_id"])
    await state.update_data(homeworks=homeworks)

    if not homeworks:
        await message.reply("По запросу ничего не нашлось")
        return

    kb = await list_keyboard(message.chat.id, 'homework', page=1, arr=homeworks)
    await update_last(state, await message.answer(text="Выберите задание, которое Вы хотите удалить",
                         reply_markup=kb))
