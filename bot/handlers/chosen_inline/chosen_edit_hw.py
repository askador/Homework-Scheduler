from bot.loader import dp, bot
from aiogram.types import ChosenInlineResult
from bot.utils.methods import edit_parse_hw
from bot.states import Inline
from aiogram.dispatcher import filters, FSMContext


@dp.chosen_inline_handler(lambda chosen_inline_query: True, state=Inline.edit)
async def chosen_edit_hw(chosen_inline_query: ChosenInlineResult, state: FSMContext):

    args = chosen_inline_query.query.split()

    s = ''
    s = s.join(args[3:])
    data = await edit_parse_hw(s, 1)
    if data == 'delete':
        await bot.send_message(state.chat, "Задание успешно удалено!\n"
                               "Предмет: {}\n"
                               "Название: {}\n"
                               "Подгруппа: {}\n".format(args[1], args[2], args[3]))
    else:
        await bot.send_message(state.chat, "Задание успешно изменено!\n"
                                           "Предмет: {}\n"
                                           "Название: {}\n"
                                           "Подгруппа: {}\n"
                                           "Срок сдачи: {}\n"
                                           "Описание: {}\n"
                                           "Приоритет: {}".format(args[1], args[2], args[3],
                                                                  data['deadline'],
                                                                  data['description'],
                                                                  data['priority']))
    await state.finish()