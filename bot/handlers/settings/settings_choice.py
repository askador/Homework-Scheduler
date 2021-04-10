from bot.loader import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram import types
from bot.keyboards import settings_keyboard_appearance, settings_keyboard_moderators, \
    settings_keyboard_subjects, settings_keyboard_subgroups, settings_keyboard_notifications, \
    settings_keyboard_terms
from bot.states import Settings
from bot.utils.methods import clear, update_last
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.types.MongoDB.Collections import Chat


@dp.callback_query_handler(state=Settings.choice)
async def callback_select_setting(callback_query: types.CallbackQuery, state: FSMContext):
    # await bot.answer_callback_query(callback_query.id)

    # await clear(state)

    markup = InlineKeyboardMarkup()
    text = 'Sample text'
    chat = Chat(callback_query.message.chat.id)

    if callback_query.data == '0':
        text = "Настройки предметов"
        await Settings.subjects.set()
        markup = await settings_keyboard_subjects()
    elif callback_query.data == '1':
        text = "Настройки подгрупп"
        await Settings.subgroups.set()
        markup = await settings_keyboard_subgroups()
    elif callback_query.data == '2':
        text = "Настройки уведомлений"
        await Settings.notifications.set()
        pin = await chat.get_field_value("can_pin")
        notify = await chat.get_field_value("notify")
        markup = await settings_keyboard_notifications(pin, notify)
    elif callback_query.data == '3':
        text = "Изменить время обновления"
        await Settings.terms.set()
        markup = await settings_keyboard_terms(await chat.get_field_value("notification_time"))
        markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back'))
        markup.add(InlineKeyboardButton('✖️ Завершить', callback_data='done'))
    elif callback_query.data == '4':
        text = "Управление модераторами"
        await Settings.moderators.set()
        markup = await settings_keyboard_moderators()
    elif callback_query.data == '5':
        text = "Настройки отображения"
        await Settings.appearance.set()
        photo = await chat.get_field_value("photo_mode")
        emoji = await chat.get_field_value("emoji_on")
        markup = await settings_keyboard_appearance(photo, emoji)
    elif callback_query.data == '6':

        # TODO implement database interaction

        await state.finish()
        text = 'Настройка завершена'
        await clear(state)

    await update_last(state, await bot.edit_message_text(text, callback_query.message.chat.id,
                                                                 callback_query.message.message_id, reply_markup=markup))
