from bot.loader import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import calendar_keyboard, edit_hw_keyboard
from bot.states import GetHomework
from bot.utils.methods import clear, update_last

from bot.types.MongoDB.Collections import Chat, Homework


@dp.callback_query_handler(lambda c: c.data is not None, state=GetHomework.choice)
async def edit_choice(callback_query: types.CallbackQuery, state: FSMContext):
    # await clear(state)
    text = 'Sample'
    markup = InlineKeyboardMarkup()

    chosen_kb = {
        "deadline":
            {
                "text": "Установите новый срок сдачи:",
                "state": GetHomework.deadline,
                "kb": await calendar_keyboard(0)
            },
        "description":
            {
                "text": "Введите новое описание:",
                "state": GetHomework.description,
                "kb": InlineKeyboardMarkup()
            }
    }

    if callback_query.data == 'common':
        chat = Chat(callback_query.message.chat.id)
        async with state.proxy() as data:
            hw = Homework(chat_id=chat.id, _id=int(data["hw_id"]))

            replace = {
                'common': 'important',
                'important': 'common'
            }
            priority = (await hw.get_info(collection='chat', by_id=True))[0]["_id"]["priority"]
            priority = replace[priority]
            await chat.update_hw(_id=int(data['hw_id']), priority=priority)
            markup = await edit_hw_keyboard(common=priority)
        await update_last(state, await bot.edit_message_text("Выберите что вы хотите отредактировать:",
                                                             callback_query.message.chat.id,
                                                             callback_query.message.message_id, reply_markup=markup))
        return
    elif callback_query.data == 'deadline':
        await state.update_data(month=0)
    elif callback_query.data == 'delete':
        text = "Задание успешно удалено"

        chat = Chat(callback_query.message.chat.id)
        await chat.update(title=callback_query.message.chat.title)

        async with state.proxy() as data:
            await chat.delete_hw(data['hw_id'])
        await clear(state)
        await update_last(state, await bot.send_message(callback_query.message.chat.id, text, reply_markup=markup))
        await state.finish()
        return
    elif callback_query.data == 'done':
        text = "Успешно завершено"

        # chat = Chat(callback_query.message.chat.id)
        # await chat.update(title=callback_query.message.chat.title)
        #
        # async with state.proxy() as data:
        #     await chat.update_hw(data['hw_id'])
        await update_last(state, await bot.send_message(callback_query.message.chat.id, text, reply_markup=markup))
        await state.finish()
        return
    # hw.edit(data['some_field'])

    text = chosen_kb[callback_query.data]['text']
    await chosen_kb[callback_query.data]['state'].set()
    markup = chosen_kb[callback_query.data]['kb']
    markup.add(InlineKeyboardButton("Назад", callback_data="back"))

    await bot.answer_callback_query(callback_query.id)
    await update_last(state, await bot.edit_message_text(text, callback_query.message.chat.id,
                                                         callback_query.message.message_id, reply_markup=markup))


@dp.message_handler(state=GetHomework.choice)
async def choice_dialogue(message, state: FSMContext):
    await clear(state)
    text = 'Sample'
    markup = InlineKeyboardMarkup()

    chosen_kb = {
        "Срок сдачи":
            {
                "text": "Установите новый срок сдачи:",
                "state": GetHomework.deadline,
                "kb": await calendar_keyboard(0)
            },
        "Описание":
            {
                "text": "Введите новое описание:",
                "state": GetHomework.description,
                "kb": InlineKeyboardMarkup()
            }
    }

    if message.text.lower() == 'Срок сдачи':
        await state.update_data(month=0)
    elif message.text.lower() == 'Удалить':
        text = "Задание успешно удалено"
        await update_last(state, await message.reply(text))
        await state.finish()
        return
    elif message.text.lower() == 'Завершить':
        await state.finish()
        return

    text = chosen_kb[message.text]['text']
    await chosen_kb[message.text]['state'].set()
    markup = chosen_kb[message.text]['kb']

    await update_last(state, await message.reply(text, reply_markup=markup))
