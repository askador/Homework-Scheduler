from bot.loader import dp, bot
from aiogram.types import ChosenInlineResult
from bot.states import Inline
from aiogram.dispatcher import FSMContext
from bot.utils.methods import user_in_chat_students


@dp.chosen_inline_handler(lambda chosen_inline_query: True)
async def chosen_delete_hw(chosen_inline_query: ChosenInlineResult):
    # print("del")
    chat_id = -1001424619068

    args = chosen_inline_query.query.split()
    await bot.send_message(chat_id,
                           "Задание успешно удалено!\n"
                           "Предмет: {}\n"
                           "Название: {}\n"
                           "Подгруппа: {}\n".format(args[1], args[2], args[3]))
