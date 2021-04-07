import os
from aiogram.types import InputMediaPhoto
from aiogram.utils.exceptions import MessageNotModified, BadRequest

from bot.loader import dp
from bot.keyboards.show_homework.show_homework import homework_kb_both
from bot.types.HomeworksList import HomeworksList
from bot.utils.methods.get_files_paths import get_files_paths


@dp.callback_query_handler(lambda call: call.data == 'next_week', state='*')
async def next_week(call, state):
    chat_id = call.message.chat.id
    show_hw_mode = ''
    async with state.proxy() as data:
        try:
            data['week_page'] += 1
            show_hw_mode = data['show_hw_mode']
        except KeyError:
            data['week_page'] = 0
            data['show_hw_mode'] = "photo"

    hws_list = HomeworksList(chat_id=chat_id, page=data['week_page'])
    await hws_list.set_fields()

    html_path, photo_path = get_files_paths(chat_id)

    if show_hw_mode == "photo":
        hw_data = await hws_list.generate_photo(html_file=html_path, photo_file=photo_path)

        try:
            await call.message.edit_media(media=InputMediaPhoto(hw_data),
                                          reply_markup=homework_kb_both)
        except MessageNotModified:
            pass
        except BadRequest:
            await call.message.delete()

            hw_data = await hws_list.generate_text()

            await call.message.answer(text=hw_data,
                                      reply_markup=homework_kb_both)

            async with state.proxy() as data:
                data['show_hw_mode'] = "text"

        os.remove(html_path)
        os.remove(photo_path)
    else:
        hw_data = await hws_list.generate_text()

        try:
            await call.message.edit_text(text=hw_data,
                                         reply_markup=homework_kb_both)
        except MessageNotModified:
            pass
        except BadRequest:
            await call.message.delete()

            hw_data = await hws_list.generate_photo(html_file=html_path, photo_file=photo_path)
            await call.message.answer_photo(hw_data, reply_markup=homework_kb_both)

            async with state.proxy() as data:
                data['show_hw_mode'] = "photo"

            os.remove(html_path)
            os.remove(photo_path)

    await call.answer(cache_time=0)

