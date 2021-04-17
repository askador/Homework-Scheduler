from bot.loader import dp
from bot.states import ChangeChat


@dp.callback_query_handler(lambda c: c.data == 'change_my_chat')
async def change_chat_id_callback(callback_query):

    await ChangeChat.new_chat_id.set()

    await callback_query.message.answer("Введите новый chat id\n"
                                        "Чтобы узнать chat id, введите <i>chat id</i> в группе с ботом")
