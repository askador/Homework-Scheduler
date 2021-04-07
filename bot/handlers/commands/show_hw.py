import os
from aiogram.dispatcher import filters

from bot.loader import dp, bot
from bot.data.commands.show_hw import COMMANDS, ALIAS
from bot.states.get_public_hw import ShowHw
from bot.keyboards.show_homework.show_homework import homework_kb_next_week
from bot.types.HomeworksList import HomeworksList
from bot.utils.methods.get_files_paths import get_files_paths
from bot.types.MongoDB.Collections import Chat


@dp.message_handler(filters.Text(startswith=ALIAS), state='*')
@dp.message_handler(filters.Command(commands=COMMANDS), state='*')
async def show_hw(message, state):
    print(message.text)
    if message.text.split() == 1 and message.text != "!п":
        return
    if message.text.split() == 2 and message.text.split()[0] != "!показать" and message.text.split()[1] != "дз":
        return

    # # Todo implement hw search
    # text_entities = message.text.replace("!показать дз", "").replace('!п', "").strip().split()
    # command_entities = [arg.strip() for arg in text_entities]
    #
    # # if text_entities[0] == "!п":
    # #     if len(text_entities) != 1:
    # #         command_entities = text_entities[1:]
    # # elif text_entities[0] == "!показать":
    # #     if len(text_entities) != 2:
    # #         command_entities = text_entities[2:]
    #
    # await message.reply(message.text.split())
    # await message.reply(command_entities)
    #
    # return

    chat_id = message.chat.id

    show_hw_mode = "text"

    if await Chat(chat_id).get_field_value("photo_mode"):
        show_hw_mode = "photo"

    if "текст" in message.text.split():
        show_hw_mode = 'text'
    elif "фото" in message.text.split():
        show_hw_mode = 'photo'

    await ShowHw.week.set()

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


