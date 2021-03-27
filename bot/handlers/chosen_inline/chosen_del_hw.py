from bot.loader import dp, bot
from aiogram.types import ChosenInlineResult
from bot.tests.tests_bot.states_test.states_test import Inline
from aiogram.dispatcher import filters, FSMContext


@dp.chosen_inline_handler(lambda chosen_inline_query: True, state=Inline.delete)
async def chosen_delete_hw(chosen_inline_query: ChosenInlineResult, state: FSMContext):
    args = chosen_inline_query.query.split()
    await bot.send_message(state.chat, "Задание успешно удалено!\n"
                                       "Предмет: {}\n"
                                       "Название: {}\n"
                                       "Подгруппа: {}\n".format(args[1], args[2], args[3]))
    await state.finish()
