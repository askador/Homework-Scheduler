from bot.loader import dp
from aiogram.types import ChatType
from bot.utils.methods import bind_student_to_chat


@dp.message_handler(commands=['start'],
                    allowed_chats=[ChatType.GROUP, ChatType.SUPERGROUP, ChatType.PRIVATE],
                    state="*")
async def start(message):

    if message.chat.type != 'private':
        await bind_student_to_chat(message.from_user.id, message.chat.id)

    await message.answer(
        f"Привет, я Homework Scheduler!\n\n"
        f"Я создан для упрощения работы с распорядком домашних заданий студентов\n"
        f"Чтобы посмотреть мой функционал введите /help"
    )
