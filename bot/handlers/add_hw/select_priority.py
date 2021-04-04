import datetime
from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.states import SetHomework
from bot.utils.methods import clear
from bot.types.MongoDB.Collections import Chat


@dp.callback_query_handler(state=SetHomework.priority)
async def set_priority(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'common' or callback_query.data == 'important':
        # await clear(state)

        await state.update_data(priority=callback_query.data)

        async with state.proxy() as data:
            await bot.edit_message_text("Задание успешно добавлено!\n\n"
                                                                   "<b>Предмет</b>: <i>{}</i>\n"
                                                                   "<b>Название</b>: <i>{}</i>\n"
                                                                   "<b>Подгруппа</b>: <i>{}</i>\n"
                                                                   "<b>Срок сдачи</b>: <i>{}</i>\n"
                                                                   "<b>Описание</b>: <i>{}</i>\n"
                                                                   "<b>Приоритет</b>: <i>{}</i>".format(
                                                                                                    data['subject'],
                                                                                                    data['name'],
                                                                                                    data['subgroup'],
                                                                                                    data['deadline'],
                                                                                                    data['description'],
                                                                                                    data['priority']),
            callback_query.message.chat.id, callback_query.message.message_id)

            chat = Chat(callback_query.message.chat.id)
            await chat.add_hw(subject=data['subject'],
                              subgroup=data['subgroup'],
                              name=data['name'],
                              description=data['description'],
                              deadline=data['deadline'],
                              priority=data['priority'])

        await state.finish()
