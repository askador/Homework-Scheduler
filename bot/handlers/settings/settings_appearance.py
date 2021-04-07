from bot.loader import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram import types
from bot.keyboards import settings_keyboard_appearance
from bot.states import Settings
from bot.utils.methods import update_last
from bot.types.MongoDB.Collections import Chat


@dp.callback_query_handler(lambda c: c.data == 'emoji', state=Settings.appearance)
async def setting_emoji(callback_query: types.CallbackQuery, state: FSMContext):
    chat = Chat(callback_query.message.chat.id)
    photo = await chat.get_field_value("photo_mode")
    photo = photo
    emoji = await chat.get_field_value("emoji_on")
    emoji = not emoji
    await chat.update(title=callback_query.message.chat.title,
                      emoji_on=emoji)
    markup = await settings_keyboard_appearance(photo, emoji)

    await update_last(state,
                      await bot.edit_message_reply_markup(callback_query.message.chat.id,
                                                          callback_query.message.message_id,
                                                          reply_markup=markup))


@dp.callback_query_handler(lambda c: c.data == 'photo', state=Settings.appearance)
async def setting_photo(callback_query: types.CallbackQuery, state: FSMContext):
    chat = Chat(callback_query.message.chat.id)
    photo = await chat.get_field_value("photo_mode")
    photo = not photo
    emoji = await chat.get_field_value("emoji_on")
    emoji = emoji
    await chat.update(title=callback_query.message.chat.title, photo_mode=photo)
    markup = await settings_keyboard_appearance(photo, emoji)

    await update_last(state,
                      await bot.edit_message_reply_markup(callback_query.message.chat.id,
                                                          callback_query.message.message_id,
                                                          reply_markup=markup))