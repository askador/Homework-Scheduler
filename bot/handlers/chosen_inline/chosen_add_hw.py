from bot.loader import dp, bot
from aiogram.types import ChosenInlineResult
from bot.utils.methods import add_parse_hw
from bot.states import Inline
from aiogram.dispatcher import filters, FSMContext


@dp.chosen_inline_handler(lambda chosen_inline_query: True, state=Inline.add)
async def chosen_add_hw(chosen_inline_query: ChosenInlineResult, state: FSMContext):

    args = chosen_inline_query.query.split()
    data = await add_parse_hw(args)
    await bot.send_message(state.chat, "Задание успешно добавлено!\n"
                           "Предмет: {}\n"
                           "Название: {}\n"
                           "Подгруппа: {}\n"
                           "Срок сдачи: {}\n"
                           "Описание: {}\n"
                           "Приоритет: {}".format(data['subj'], data['name'],
                                                  data['subg'],
                                                  data['deadline'],
                                                  data['description'],
                                                  data['priority']))
    await state.finish()

