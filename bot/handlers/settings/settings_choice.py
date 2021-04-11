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
    if callback_query.data == '6':
        await state.finish()
        await clear(state)
        return

    chat = Chat(callback_query.message.chat.id)

    chosen_kb = {
        "0": {
            "text": "Настройки предметов",
            "state": Settings.subjects,
            "kb": await settings_keyboard_subjects()
        },
        "1": {
            "text": "Настройки подгрупп",
            "state": Settings.subgroups,
            "kb": await settings_keyboard_subgroups()
        },
        "2": {
            "text": "Настройки уведомлений",
            "state": Settings.notifications,
            "kb": await settings_keyboard_notifications(pin=await chat.get_field_value("can_pin"),
                                                        notify=await chat.get_field_value("notify"))
        },
        "3": {
            "text": "Изменить время обновления",
            "state": Settings.terms,
            "kb": await settings_keyboard_terms(selected=await chat.get_field_value("notification_time"))
        },
        "4": {
            "text": "Управление модераторами",
            "state": Settings.moderators,
            "kb": await settings_keyboard_moderators(),
        },
        "5": {
            "text": "Настройки отображения",
            "state": Settings.appearance,
            "kb": await settings_keyboard_appearance(photo=await chat.get_field_value("photo_mode"),
                                                     emoji=await chat.get_field_value("emoji_on"))
        },
    }

    text = chosen_kb[callback_query.data]['text']
    await chosen_kb[callback_query.data]['state'].set()
    kb = chosen_kb[callback_query.data]['kb']

    await update_last(state,
                      await callback_query.message.edit_text(text, reply_markup=kb)
                      )