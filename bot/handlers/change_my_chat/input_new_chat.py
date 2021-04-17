from bot.loader import dp
from bot.states import ChangeChat
from bot.types.MongoDB import Chat
from bot.utils.methods import user_in_chat_students


@dp.message_handler(state=ChangeChat.new_chat_id)
async def input_new_chat_id(message, state):
    user_id = message.from_user.id
    new_chat_id = message.text

    if not new_chat_id.startswith('-100'):
        await message.reply("Такой группы не сущесвует")

        return

    chat = Chat(new_chat_id)
    title = await chat.get_field_value('title')

    if not title:
        await message.reply("Данный чат не зарегистрирован ботом")

        return

    old_chat = Chat(await user_in_chat_students(user_id))
    old_chat_students = await old_chat.get_field_value('students')
    old_chat_students.remove(user_id)
    await old_chat.update(students=old_chat_students)

    new_chat = Chat(new_chat_id)
    new_chat_students = await new_chat.get_field_value('students')
    new_chat_students.append(int(user_id))
    await new_chat.update(students=new_chat_students)

    new_chat_title = new_chat.get_field_value('title')

    await message.reply(f"Вы успешно сменили группу!\n"
                        f"Название: {new_chat_title}\n"
                        f"Id: {new_chat_id}")
    await state.finish()

