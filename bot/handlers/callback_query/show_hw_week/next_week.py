import os
from aiogram.types import InputMediaPhoto
from aiogram.utils.exceptions import MessageNotModified
from pprint import pprint

from bot.loader import dp, bot
from bot.states.get_public_hw import ShowHw
from bot.keyboards.show_homework.show_homework import homework_kb_both
from bot.types.HomeworksList import HomeworksList
from bot.utils.methods.get_files_pathes import get_files_pathes


@dp.callback_query_handler(lambda call: call.data == 'next_week')
async def next_week(call, state):
    message_id = call.message.message_id
    chat_id = call.message.chat.id
    async with state.proxy() as data:
        try:
            if data['week_page']:
                pass
        except KeyError:
            data['week_page'] = 0
        else:
            data['week_page'] += 1

        html_path, photo_path = get_files_pathes(chat_id)

        hws_list = HomeworksList(chat_id=chat_id, page=data['week_page'])
        await hws_list.set_fields()

        hw_photo = await hws_list.generate_photo(html_file=html_path, photo_file=photo_path)

        await call.answer(cache_time=0)
        try:
            await bot.edit_message_media(media=InputMediaPhoto(hw_photo),
                                         chat_id=chat_id,
                                         message_id=message_id,
                                         reply_markup=homework_kb_both)
        except MessageNotModified:
            pass

    os.remove(html_path)
    os.remove(photo_path)
