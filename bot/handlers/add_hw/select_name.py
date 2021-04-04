import datetime
from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import subjects_keyboard, calendar_keyboard, subgroups_keyboard, list_keyboard
from bot.states import SetHomework
from bot.utils.methods import clear, update_last, check_date, make_datetime, check_callback_date, check_precise
# from datetime import datetime, timedelta
from bot.types.MongoDB.Collections import Chat


@dp.message_handler(state=SetHomework.name)
async def select_name(message: types.Message, state: FSMContext):
    hw_name = message.text

    SUBGROUPS = await Chat(message.chat.id).get_field_value("subgroups")
    print('name')
    # await clear(state)

    await state.update_data(name=hw_name)
    await SetHomework.next()
    await state.update_data(month=0)
    print('issue1')

    markup = await list_keyboard(message.chat.id, 'subgroup', 1)
    print('issue2')

    async with state.proxy() as data:
        await update_last(state, await bot.edit_message_text("Выберите подгруппу:", message.chat.id,
                                                         data['last_message_id'], reply_markup=markup))


    print('issue0')