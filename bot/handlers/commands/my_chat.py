from aiogram.dispatcher.filters import Command

from bot.loader import dp, bot
from bot.data.commands.my_chat import COMMANDS
from bot.utils.methods import user_in_chat_students
from bot.types.MongoDB import Chat
from bot.keyboards import change_my_chat_kb


@dp.message_handler(Command(commands=COMMANDS))
async def my_chat(message):
    my_chat_id = await user_in_chat_students(message.from_user.id)

    if not my_chat_id:
        await message.reply("Вы не привязаны ни к какой группе\n"
                            "Воспользуйтесь командой /start@itai_hw_bot в группе с ботом")

        return

    chat = Chat(my_chat_id)
    title = await chat.get_field_value('title')

    await bot.send_message(message.chat.id,
                           text=f"Вы привязаны к {title}\n"
                                f"Id: {my_chat_id}",
                           parse_mode=None,
                           reply_markup=change_my_chat_kb)
    # await message.answer(f"Вы привязаны к {title}\n"
    #                      f"chat_id: {my_chat_id}",
    #                      change_my_chat_kb, parse_mode=None)
