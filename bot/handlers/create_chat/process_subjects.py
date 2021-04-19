from bot.loader import dp
from bot.scheduler import scheduler
from bot.states import AddChat
from bot.utils.methods import bind_student_to_chat
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@dp.message_handler(state=AddChat.subjects)
async def process_subjects(message, state):
    await bind_student_to_chat(message.from_user.id, message.chat.id)

    subjects = message.text.split(',')
    filtered_subjects = []

    for subject in subjects:
        if subject.strip() != '':
            filtered_subjects.append(subject.strip())

    async with state.proxy() as data:
        data['chat_subjects'] = filtered_subjects

    none_keyboard = InlineKeyboardMarkup(row_width=1)
    none_keyboard.add(InlineKeyboardButton(text="None", callback_data="none"))

    await AddChat.next()
    await message.answer("Теперь введите название ваших подгруппы через запятую.\n"
                         "Нажмите None если их нету", reply_markup=none_keyboard)
