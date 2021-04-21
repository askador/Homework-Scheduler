from bot.loader import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram import types
from bot.keyboards import settings_keyboard, list_keyboard
from bot.states import Settings
from bot.utils.methods import clear, update_last
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.types.MongoDB.Collections import Chat


@dp.callback_query_handler(lambda c: c.data == 'add', state=Settings.subgroups)
async def subgroup_add(callback_query: types.CallbackQuery, state: FSMContext):
    # await clear(state)
    await Settings.add_subgroups.set()
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back'))
    markup.add(InlineKeyboardButton('✖️ Завершить', callback_data='done'))
    await update_last(state,
                      await bot.edit_message_text("Введите список новых подгрупп через запятую", callback_query.message.chat.id,
                                                         callback_query.message.message_id, reply_markup=markup))


@dp.message_handler(state=Settings.add_subgroups)
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

    await Settings.remove_subgroups.set()
    chat = Chat(callback_query.message.chat.id)
    await state.update_data(page=1, special=await chat.get_field_value('subgroups'), to_display=[])
    async with state.proxy() as data:
        markup = await list_keyboard(callback_query.message.chat.id, 'special', data['page'], data['special'])
    markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back'))
    markup.add(InlineKeyboardButton('✖️ Завершить', callback_data='done'))
    await update_last(state,
                      await bot.edit_message_text("Удалить подгруппы", callback_query.message.chat.id,
                                                         callback_query.message.message_id, reply_markup=markup))


@dp.callback_query_handler(lambda c: c.data.isdigit(), state=Settings.remove_subgroups)
async def picked_subgroup(callback_query: types.CallbackQuery, state: FSMContext):
    chat = Chat(callback_query.message.chat.id)

    subg_id = int(callback_query.data)
    async with state.proxy() as data:
        subgroups = data['special']
        data['to_display'] += [subgroups[subg_id]]
        subgroups.pop(subg_id)
        data['special'] = subgroups
        markup = await list_keyboard(callback_query.message.chat.id, 'special', data['page'], data['special'])
        markup.add(InlineKeyboardButton('⏪ Отменить', callback_data='redo'))
        markup.add(InlineKeyboardButton('✅ Сохранить изменения', callback_data='save'))
        to_display = ""
        for i in range(len(data['to_display'])-1):
            to_display += data['to_display'][i] + ', '
        to_display += data['to_display'][len(data['to_display'])-1]
        await update_last(state,
                          await bot.edit_message_text("Удалить подгруппы \n Выбраны:{}".format(to_display), callback_query.message.chat.id,
                                                      callback_query.message.message_id, reply_markup=markup))


@dp.callback_query_handler(lambda c: c.data == 'redo', state=Settings.remove_subgroups)
async def redo_subject(callback_query: types.CallbackQuery, state: FSMContext):
    chat = Chat(callback_query.message.chat.id)

    async with state.proxy() as data:
        data['special'] += [data['to_display'].pop()]
        markup = await list_keyboard(callback_query.message.chat.id, 'special', data['page'], data['special'])
        if len(data['to_display']) != 0:
            markup.add(InlineKeyboardButton('⏪ Отменить', callback_data='redo'))
        markup.add(InlineKeyboardButton('Сохранить изменения', callback_data='save'))
        to_display = ""
        if len(data['to_display']) != 0:
            for i in range(len(data['to_display'])-1):
                to_display += data['to_display'][i] + ', '
            to_display += data['to_display'][len(data['to_display'])-1]
            await update_last(state,
                              await bot.edit_message_text("Удалить подгруппы \n Выбраны:{}".format(to_display), callback_query.message.chat.id,
                                                          callback_query.message.message_id, reply_markup=markup))
        else:
            await update_last(state,
                              await bot.edit_message_text("Удалить подгруппы",
                                                          callback_query.message.chat.id,
                                                          callback_query.message.message_id, reply_markup=markup))


@dp.callback_query_handler(lambda c: c.data == 'save', state=Settings.remove_subgroups)
async def save_changes(callback_query: types.CallbackQuery, state: FSMContext):
    # Todo
    # deleting, checking for hw

    groups = callback_query.message.text.replace("Выбраны:", '').replace("Удалить подгруппы \n", '').split(',')
    groups = [group.strip() for group in groups]

    await clear(state)

    chat = Chat(callback_query.message.chat.id)

    text = ''

    for group in groups:
        hw = await chat.get_homeworks(filters=[{"homeworks.subgroup": group}])
        if hw:
            text += f"Еще остались задания для <b>{group}</b> подгруппы"
            break

    if text == '':
        text = "Удалено!\nМеню настроек"

        subgroups = await chat.get_field_value('subgroups')
        for group in groups:
            subgroups.remove(group)

        await chat.update(subgroups=subgroups)

    await Settings.choice.set()
    markup = await settings_keyboard()
    await update_last(state, await bot.send_message(callback_query.message.chat.id, text,
                                                    reply_markup=markup))


@dp.callback_query_handler(lambda c: c.data == 'edit', state=Settings.subgroups)
async def subgroup_edit(callback_query: types.CallbackQuery, state: FSMContext):
    # await clear(state)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back'))
    markup.add(InlineKeyboardButton('✖️ Завершить', callback_data='done'))
    await update_last(state,
                      await bot.edit_message_text("Изменить состав подгруппы", callback_query.message.chat.id,
                                                         callback_query.message.message_id, reply_markup=markup))
