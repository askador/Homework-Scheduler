from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import filters, FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import subjects_keyboard, calendar_keyboard, subgroups_keyboard, list_keyboard
from bot.states import SetHomework
from bot.utils.methods import  update_last
from bot.types.MongoDB.Collections import Chat


@dp.message_handler(state=SetHomework.name)
async def select_name(message: types.Message, state: FSMContext):
    hw_name = message.text

    SUBGROUPS = await Chat(message.chat.id).get_field_value("subgroups")
    # await clear(state)

    await state.update_data(name=hw_name)
    await SetHomework.next()
    await state.update_data(month=0)

    markup = await list_keyboard(message.chat.id, 'subgroup', 1)

    async with state.proxy() as data:
        await update_last(state, await bot.send_message(message.chat.id, "Выберите подгруппу:",
                                                             reply_markup=markup))


