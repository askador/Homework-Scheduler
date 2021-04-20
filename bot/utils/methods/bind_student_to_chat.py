from bot.types.MongoDB import Chat
from bot.utils.methods import user_in_chat_students


async def bind_student_to_chat(user_id, chat_id):

    if await user_in_chat_students(user_id):
        return

    chat = Chat(chat_id)
    chat_students = await chat.get_field_value('students')

    if not chat_students:
        return

    already_in_chat = user_id in chat_students

    if already_in_chat:
        return

    chat_students += [user_id]
    await chat.update(students=chat_students)

