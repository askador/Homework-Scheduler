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


@dp.callback_query_handler(lambda c: c.data.isdigit(), state=Settings.terms)
async def set_term(callback_query: types.CallbackQuery, state: FSMContext):
    # await clear(state)
    chat = Chat(callback_query.message.chat.id)

    await chat.update(title=callback_query.message.chat.title, notification_time=int(callback_query.data))

    markup = await select_time_keyboard(await chat.get_field_value("notification_time"))
    markup.add(InlineKeyboardButton('Назад', callback_data='back'))
    markup.add(InlineKeyboardButton('Завершить', callback_data='done'))
    await update_last(state,
                      await bot.edit_message_text("Изменить время обновления",
                                                             callback_query.message.chat.id,
                                                             callback_query.message.message_id,
                                                             reply_markup=markup))



