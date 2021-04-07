from bot.loader import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram import types
from bot.keyboards import settings_keyboard, list_keyboard
from bot.states import Settings
from bot.utils.methods import clear, update_last
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.types.MongoDB.Collections import Chat


@dp.callback_query_handler(lambda c: c.data == 'add', state=Settings.subjects)
async def subject_add(callback_query: types.CallbackQuery, state: FSMContext):
    # await clear(state)
    await Settings.add_subjects.set()
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back'))
    markup.add(InlineKeyboardButton('✖️ Завершить', callback_data='done'))
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

    await Settings.remove_subjects.set()
    chat = Chat(callback_query.message.chat.id)
    await state.update_data(page=1, subjects=await chat.get_field_value('subjects'), to_display=[])
    async with state.proxy() as data:
        markup = await list_keyboard(callback_query.message.chat.id, 'special', data['page'], data['subjects'])
    markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back'))
    markup.add(InlineKeyboardButton('✖️ Завершить', callback_data='done'))
    await update_last(state,
                      await bot.edit_message_text("Удалить предметы", callback_query.message.chat.id,
                                                         callback_query.message.message_id, reply_markup=markup))


@dp.callback_query_handler(lambda c: c.data.isdigit(), state=Settings.remove_subjects)
async def picked_subject(callback_query: types.CallbackQuery, state: FSMContext):
    chat = Chat(callback_query.message.chat.id)

    subj_id = int(callback_query.data)
    async with state.proxy() as data:
        subjects = data['subjects']
        data['to_display'] += [subjects[subj_id]]
        subjects.pop(subj_id)
        data['subjects'] = subjects
        markup = await list_keyboard(callback_query.message.chat.id, 'special', data['page'], data['subjects'])
        markup.add(InlineKeyboardButton('Сохранить изменения', callback_data='save'))
        to_display = ""
        for i in range(len(data['to_display'])-1):
            to_display += data['to_display'][i] + ', '
        to_display += data['to_display'][len(data['to_display'])-1]
        await update_last(state,
                          await bot.edit_message_text("Удалить предметы \n Выбраны:{}".format(to_display), callback_query.message.chat.id,
                                                      callback_query.message.message_id, reply_markup=markup))


@dp.callback_query_handler(lambda c: c.data == 'save', state=Settings.remove_subjects)
async def save_changes(callback_query: types.CallbackQuery, state: FSMContext):
    # Todo
    # deleting, checking for hw

    await clear(state)

    await Settings.choice.set()
    markup = await settings_keyboard()
    await update_last(state, await bot.send_message(callback_query.message.chat.id, "Удалено!\nМеню настроек",
                                                    reply_markup=markup))