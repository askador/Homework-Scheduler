from bot.loader import dp, bot
from bot.states import GetHomework
from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.utils.methods import update_last
from bot.keyboards import edit_hw_keyboard
from bot.types.MongoDB.Collections import Chat, Homework


@dp.callback_query_handler(lambda c: c.data == 'back', state=[GetHomework.deadline, GetHomework.description])
@dp.callback_query_handler(lambda c: c.data is not None, state=GetHomework.homework)
async def callback_select_homework(callback_query: types.CallbackQuery, state: FSMContext):
    # await clear(state)
    chat = Chat(callback_query.message.chat.id)
    hw = Homework(chat_id=chat.id, _id=int(callback_query.data))

    if callback_query.data.isdigit():
        await state.update_data(hw_id=callback_query.data, page=1)
    await bot.answer_callback_query(callback_query.id)
    await GetHomework.choice.set()
    priority = await hw.get_info(collection='chat', by_id=True)

    print(priority)

    markup = await edit_hw_keyboard(common=priority[0]["_id"]["priority"])

    await update_last(state, await bot.edit_message_text("Выберите что вы хотите отредактировать:",
                                                         callback_query.message.chat.id,
                                                         callback_query.message.message_id, reply_markup=markup)
                      )




