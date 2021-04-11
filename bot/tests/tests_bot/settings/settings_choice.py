from bot.loader import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram import types

from bot.states import Settings
from bot.utils.methods import clear
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.types.MongoDB.Collections import Chat

from bot.tests.tests_bot.settings.settings_keyboard import settings_keyboard_subjects

# async def chosen_kb(set_state, markup):
#


@dp.callback_query_handler(state=Settings.choice)
async def callback_select_setting(callback_query: types.CallbackQuery, state: FSMContext):
    print("settings choice")
    # markup = InlineKeyboardMarkup()

    # text = 'Sample text'
    chat = Chat(callback_query.message.chat.id)

    chosen_kb = {
        "subj_settings": {
            "text": "предметов",
            "state": Settings.subjects,
            "kb": await settings_keyboard_subjects()
        },
        # "subgr_settings": "",
        # "notifications_settings": "",
        # "terms_settings": "",
        # "style_settings": "",
    }

    text = chosen_kb[callback_query.data]['text']
    await chosen_kb[callback_query.data]['state'].set()
    kb = chosen_kb[callback_query.data]['kb']

    # if callback_query.data == 'subj_settings':
    #     text = "Настройки предметов"
    #     await Settings.subjects.set()
    #     markup = await settings_keyboard_subjects()
    # elif callback_query.data == 'subgr_settings':
    #     text = "Настройки подгрупп"
    #     await Settings.subgroups.set()
    #     markup = await settings_keyboard_subgroups()
    # elif callback_query.data == 'notifications_settings':
    #     text = "Настройки уведомлений"
    #     await Settings.notifications.set()
    #     markup = await settings_keyboard_notifications(pin=await chat.get_field_value("can_pin"))
    # elif callback_query.data == 'terms_settings':
    #     text = "Изменить время обновления"
    #     await Settings.terms.set()
    #     markup = await settings_keyboard_terms(selected=await chat.get_field_value("notification_time"))
    # elif callback_query.data == 'style_settings':
    #     text = "Настройки отображения"
    #     await Settings.appearance.set()
    #     markup = await settings_keyboard_appearance(photo=await chat.get_field_value("photo_mode"),
    #                                                 emoji=await chat.get_field_value("emoji_on"))
    if callback_query.data == 'close_settings':
        await state.finish()
        await clear(state)

    await bot.edit_message_text(text,
                                callback_query.message.chat.id,
                                callback_query.message.message_id,
                                reply_markup=kb)
