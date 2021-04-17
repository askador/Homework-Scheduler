import os
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardButton

from bot.loader import dp, bot
from bot.data.commands.show_hw import COMMANDS, COMMANDS_TEXT
from bot.states.get_public_hw import ShowHw
from bot.keyboards import list_keyboard
from bot.keyboards.show_homework.show_homework import homework_kb_next_week
from bot.types.HomeworksList import HomeworksList
from bot.utils.methods import get_files_paths, bind_student_to_chat
from bot.types.MongoDB.Collections import Chat


@dp.message_handler(Command(commands=COMMANDS), state='*')
@dp.message_handler(Command(commands=COMMANDS_TEXT, prefixes="!"), state='*')
async def show_hw(message, state):
    await bind_student_to_chat(message.from_user.id, message.chat.id)

    chat_id = message.chat.id
    chat = Chat(chat_id)

    show_hw_mode = "text"

    args = message.get_args().split() if message.is_command() else message.text.split()[1:]

    if await chat.get_field_value("photo_mode"):
        show_hw_mode = "photo"

    if "текст" in args and len(args) == 1:
        show_hw_mode = 'text'
        del args[0]
    elif "фото" in args and len(args) == 1:
        show_hw_mode = 'photo'
        del args[0]
    await ShowHw.week.set()

    if args:
        if 'фото' not in args or 'текст' not in args:
            state = dp.get_current().current_state()
            await state.update_data(page=1)

            homeworks = sorted(await chat.homeworks_search(args=args, full_info=False), key=lambda x: x["_id"]["_id"])

            if not homeworks:
                await message.reply("По запросу ничего не нашлось")
                return

            kb = await list_keyboard(message.chat.id, 'homework', page=1, arr=homeworks)
            kb.add(InlineKeyboardButton(text="✖️ Закрыть", callback_data="close"))
            await message.answer(text="Выберите задание для просмотра",
                                 reply_markup=kb)

            return

    async with state.proxy() as data:
        data['show_hw_mode'] = show_hw_mode
        data['week_page'] = 0

    """Generate homeworks"""
    loading = await message.reply("Загрузка...")

    hws_list = HomeworksList(chat_id=chat_id, page=0)
    await hws_list.set_fields()

    if show_hw_mode == "photo":
        html_path, photo_path = get_files_paths(chat_id)
        hw_data = await hws_list.generate_photo(html_file=html_path, photo_file=photo_path)

        await bot.delete_message(chat_id=chat_id, message_id=loading.message_id)
        await message.answer_photo(hw_data, reply_markup=homework_kb_next_week)

        os.remove(html_path)
        os.remove(photo_path)
    else:
        hw_data = await hws_list.generate_text()

        await bot.delete_message(chat_id=chat_id, message_id=loading.message_id)
        await message.answer(hw_data, reply_markup=homework_kb_next_week)

    await message.delete()
