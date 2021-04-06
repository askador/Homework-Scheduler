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


@dp.callback_query_handler(lambda c: c.data == 'add', state=Settings.subgroups)
async def subgroup_add(callback_query: types.CallbackQuery, state: FSMContext):
    # await clear(state)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Назад', callback_data='back'))
    markup.add(InlineKeyboardButton('Завершить', callback_data='done'))
    await update_last(state,
                      await bot.edit_message_text("Введите список новых подгрупп через запятую", callback_query.message.chat.id,
                                                         callback_query.message.message_id, reply_markup=markup))


@dp.message_handler(state=Settings.subgroups)
async def add_subjects(message: types.Message, state: FSMContext):
    await clear(state)

    subgs = message.text.split(',')
    filtered_subgroups = []

    for subgroup in subgs:
        if subgroup.strip() != '':
            filtered_subgroups.append(subgroup.strip())

    chat = Chat(message.chat.id)
    subgroups = await chat.get_field_value('subgroups') + filtered_subgroups
    await chat.update(title=message.chat.title, subgroups=subgroups)

    await Settings.choice.set()
    markup = await settings_keyboard()
    await update_last(state, await bot.send_message(message.chat.id, "Добавлено!\nМеню настроек",
                                                    reply_markup=markup))



@dp.callback_query_handler(lambda c: c.data == 'remove', state=Settings.subgroups)
async def subgroup_remove(callback_query: types.CallbackQuery, state: FSMContext):
    # await clear(state)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Назад', callback_data='back'))
    markup.add(InlineKeyboardButton('Завершить', callback_data='done'))
    await update_last(state,
                      await bot.edit_message_text("Удалить подгруппу", callback_query.message.chat.id,
                                                         callback_query.message.message_id, reply_markup=markup))


@dp.callback_query_handler(lambda c: c.data == 'edit', state=Settings.subgroups)
async def subgroup_edit(callback_query: types.CallbackQuery, state: FSMContext):
    # await clear(state)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Назад', callback_data='back'))
    markup.add(InlineKeyboardButton('Завершить', callback_data='done'))
    await update_last(state,
                      await bot.edit_message_text("Изменить состав подгруппы", callback_query.message.chat.id,
                                                         callback_query.message.message_id, reply_markup=markup))
