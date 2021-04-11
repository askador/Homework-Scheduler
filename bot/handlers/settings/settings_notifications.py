from bot.loader import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram import types
from bot.keyboards import settings_keyboard_notifications
from bot.states import Settings
from bot.utils.methods import update_last
from bot.types.MongoDB.Collections import Chat


@dp.callback_query_handler(lambda c: c.data == 'pin', state=Settings.notifications)
async def setting_pin(callback_query: types.CallbackQuery, state: FSMContext):
    chat = Chat(callback_query.message.chat.id)
    pin = await chat.get_field_value("can_pin")
    notify = await chat.get_field_value("notify")
    pin = not pin
    await chat.update(title=callback_query.message.chat.title, can_pin=pin)
    markup = await settings_keyboard_notifications(pin, notify)

    await update_last(state,
                      await bot.edit_message_reply_markup(callback_query.message.chat.id,
                                                          callback_query.message.message_id,
                                                          reply_markup=markup))


@dp.callback_query_handler(lambda c: c.data == 'notify', state=Settings.notifications)
async def setting_pin(callback_query: types.CallbackQuery, state: FSMContext):
    chat = Chat(callback_query.message.chat.id)
    pin = await chat.get_field_value("can_pin")
    notify = await chat.get_field_value("notify")
    notify = not notify
    await chat.update(title=callback_query.message.chat.title, notify=notify)
    markup = await settings_keyboard_notifications(pin, notify)

    await update_last(state,
                      await bot.edit_message_reply_markup(callback_query.message.chat.id,
                                                          callback_query.message.message_id,
                                                          reply_markup=markup))
