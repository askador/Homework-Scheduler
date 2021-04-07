from bot.loader import dp, bot
from aiogram.dispatcher import filters, FSMContext
from aiogram import types
from bot.keyboards import select_time_keyboard, settings_keyboard_appearance, settings_keyboard_moderators, \
    settings_keyboard, settings_keyboard_subjects, settings_keyboard_subgroups, settings_keyboard_notifications, \
    settings_keyboard_terms
from bot.states import Settings
from bot.utils.methods import clear, update_last
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .test import COMMANDS, CHAT_TYPES, ALIAS
from bot.types.MongoDB.Collections import Chat


@dp.callback_query_handler(lambda c: c.data == 'add', state=Settings.subjects)
async def subject_add(callback_query: types.CallbackQuery, state: FSMContext):
    # await clear(state)
    await Settings.add_subjects.set()
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Назад', callback_data='back'))
    markup.add(InlineKeyboardButton('Завершить', callback_data='done'))
    """await callback_query.message.edit_text(
        text="dsf",
        reply_markup=markup
    )"""
    await update_last(state,
                      await bot.edit_message_text(
                          "Введите список новых предметов через запятую",
                          callback_query.message.chat.id,
                          callback_query.message.message_id,
                          reply_markup=markup))


@dp.message_handler(state=Settings.add_subjects)
async def add_subjects(message: types.Message, state: FSMContext):
    await clear(state)

    subjs = message.text.split(',')
    filtered_subjects = []

    for subject in subjs:
        if subject.strip() != '':
            filtered_subjects.append(subject.strip())

    chat = Chat(message.chat.id)
    subjects = await chat.get_field_value('subjects') + filtered_subjects
    await chat.update(title=message.chat.title, subjects=subjects)

    await Settings.choice.set()
    markup = await settings_keyboard()
    await update_last(state, await bot.send_message(message.chat.id, "Добавлено!\nМеню настроек",
                                                    reply_markup=markup))


@dp.callback_query_handler(lambda c: c.data == 'remove', state=Settings.subjects)
async def subject_remove(callback_query: types.CallbackQuery, state: FSMContext):
    # await clear(state)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Назад', callback_data='back'))
    markup.add(InlineKeyboardButton('Завершить', callback_data='done'))
    await update_last(state,
                      await bot.edit_message_text("Удалить предметы", callback_query.message.chat.id,
                                                         callback_query.message.message_id, reply_markup=markup))