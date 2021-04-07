from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.states import SetHomework
from bot.utils.methods import clear, update_last


@dp.message_handler(state=SetHomework.description)
async def select_description(message: types.Message, state: FSMContext):
    hw_description = message.text

    await clear(state)

    await state.update_data(description=hw_description)
    await SetHomework.priority.set()

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('❕ Обычное', callback_data='common'))
    markup.add(InlineKeyboardButton('❗️Важное', callback_data='important'))

    async with state.proxy() as data:
        await update_last(state, await bot.send_message(message.chat.id, 'Уточните важность задания',
                                                        reply_markup=markup))