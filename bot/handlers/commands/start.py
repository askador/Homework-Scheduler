from bot.loader import dp
from aiogram.types import ChatType


@dp.message_handler(commands=['start'],
                    allowed_chats=[ChatType.GROUP, ChatType.SUPERGROUP, ChatType.PRIVATE],
                    state="*")
async def start(message):

    await message.answer(
        f"Привет, я Homework Scheduler!\n"
        f"Я создан для упрощения работы с распорядком домашних заданий студентов\n"
        f"Чтобы посмотреть мой функционал введите /help"
    )
