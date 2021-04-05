from bot.loader import dp, bot
from bot.states import GetHomework
from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from bot.utils.methods import update_last
from bot.keyboards import edit_hw_keyboard


@dp.callback_query_handler(lambda c: c.data is not None, state=GetHomework.homework)
async def callback_select_homework(callback_query: types.CallbackQuery, state: FSMContext):
    # await clear(state)
    await state.update_data(id=callback_query.data, page=0)
    await bot.answer_callback_query(callback_query.id)
    await GetHomework.choice.set()
    markup = await edit_hw_keyboard()

    await update_last(state, await bot.edit_message_text("Выберите что вы хотите отредактировать:",
                                                         callback_query.message.chat.id,
                                                         callback_query.message.message_id, reply_markup=markup))