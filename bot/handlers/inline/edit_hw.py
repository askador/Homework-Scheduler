from bot.loader import dp, bot
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from aiogram.dispatcher import filters, FSMContext
from bot.utils.methods import edit_parse_hw
from bot.tests.tests_bot.states_test.states_test import Inline

TEST = [
    '1'
]

ANSWERS = {
    'delete': 'удалить дз!',
    'date_error': 'неверно указана дата!',
    'prior_error': 'неверно указан приоритет!',
}


@dp.inline_handler(filters.Text(startswith=['edit_hw']))
@dp.inline_handler(filters.Text(startswith=['edit_hw']), state=Inline.edit)
async def inline_edit_hw(inline_query: InlineQuery, state: FSMContext):
    args = inline_query.query.split()
    print(args)
    await state.finish()

    n = 'ok'

    hw = 'kek'

    if len(args) == 1:
        hw = 'предмет название подгруппа'
    elif len(args) >= 2:
        if args[1] in TEST:
            if len(args) >= 4:
                if args[3] in TEST or args[3] == 'все':
                    hw = 'можно менять!'
                    s = ' '
                    s = s.join(args[3:])
                    n = await edit_parse_hw(s, 0)
                else:
                    hw = 'подгруппа введена неверно!'
            else:
                hw = 'предмет название подгруппа'
        else:
            hw = 'предмет введен неверно!'
    else:
        pass

    if n != 'ok':
        hw = ANSWERS[n]
    else:
        await Inline.edit.set()

    input_content = InputTextMessageContent(hw)
    result_id = '1'
    item = InlineQueryResultArticle(
        title='edit_hw:',
        id=result_id,
        description=f'{hw!r}',
        input_message_content=input_content,
    )
    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)