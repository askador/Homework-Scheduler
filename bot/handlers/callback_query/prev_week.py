import os
from aiogram.types import InputMediaPhoto

from bot.loader import dp, bot
from bot.keyboards.show_homework.show_homework import homework_kb_next_week, homework_kb_both
from bot.states.get_public_hw import ShowHw
from bot.types.HomeworksList import HomeworksList
from bot.utils.methods.get_files_pathes import get_files_pathes


@dp.callback_query_handler(lambda call: call.data == 'prev_week')
async def prev_week(call, state):
    message_id = call.message.message_id
    chat_id = call.message.chat.id

    kb = homework_kb_both
    async with state.proxy() as data:
        try:
            if data['week_page']:
                pass
        except KeyError:
            data['week_page'] = 0
        else:
            data['week_page'] -= 1

        if data['week_page'] == 0:
            kb = homework_kb_next_week

        hws_list = HomeworksList(chat_id=chat_id, page=data['week_page'])
        await hws_list.set_fields()

        html_path, photo_path = get_files_pathes(chat_id)

        hw_photo = await hws_list.generate_photo(html_file=html_path, photo_file=photo_path)

        await call.answer(cache_time=0)
        await bot.edit_message_media(media=InputMediaPhoto(hw_photo),
                                     chat_id=chat_id,
                                     message_id=message_id,
                                     reply_markup=kb)

    os.remove(html_path)
    os.remove(photo_path)