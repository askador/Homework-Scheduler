from bot.loader import dp, bot
from aiogram.dispatcher import filters, FSMContext
from aiogram import types
from bot.keyboards import select_time_keyboard, settings_keyboard_appearance, settings_keyboard_moderators, \
    settings_keyboard, settings_keyboard_subjects, settings_keyboard_subgroups, settings_keyboard_notifications, \
    settings_keyboard_terms
from bot.states import Settings
from bot.utils.methods import clear, update_last
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.types.MongoDB.Collections import Chat


@dp.callback_query_handler(lambda c: c.data == 'pin', state=Settings.notifications)
async def setting_pin(callback_query: types.CallbackQuery, state: FSMContext):
    chat = Chat(callback_query.message.chat.id)
    pin = await chat.get_field_value("can_pin")
    print(type(pin))
    pin = not pin
    await chat.update(title=callback_query.message.chat.title, can_pin=pin)
    markup = await settings_keyboard_notifications(pin)

    await update_last(state,
                      await bot.edit_message_reply_markup(callback_query.message.chat.id,
                                                          callback_query.message.message_id,
                                                          reply_markup=markup))
