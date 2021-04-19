from bot.loader import dp, bot
from aiogram.types import ChosenInlineResult
from bot.utils.methods import add_parse_hw
from bot.states import Inline
from aiogram.dispatcher import FSMContext
from bot.utils.methods import user_in_chat_students


@dp.chosen_inline_handler(lambda chosen_inline_query: True)
async def chosen_add_hw(chosen_inline_query: ChosenInlineResult):
    # print("add")
    chat_id = -1001424619068
    args = chosen_inline_query.query.split()
    data = await add_parse_hw(args)
    await bot.send_message(chat_id,
                           "Задание успешно добавлено!\n"
                           "Предмет: {}\n"
                           "Название: {}\n"
                           "Подгруппа: {}\n"
                           "Срок сдачи: {}\n"
                           "Описание: {}\n"
                           "Приоритет: {}".format(data['subj'], data['name'],
                                                  data['subgroup'],
                                                  data['deadline'],
                                                  data['description'],
                                                  data['priority']))
