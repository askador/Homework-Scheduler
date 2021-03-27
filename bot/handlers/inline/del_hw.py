from bot.loader import dp, bot
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from aiogram.dispatcher import filters, FSMContext
from bot.tests.tests_bot.states_test.states_test import Inline

TEST = [
    "1"
]


@dp.inline_handler(filters.Text(startswith=['del_hw']))
@dp.inline_handler(filters.Text(startswith=['del_hw']), state=Inline.delete)
async def inline_del_hw(inline_query: InlineQuery, state: FSMContext):
    await state.finish()
    args = inline_query.query.split()
    print(args)

    hw = 'kek'

    if len(args) == 1:
        hw = 'предмет название подгруппа'
    elif len(args) >= 2:
        if args[1] in TEST:
            if len(args) >= 4:
                if args[3] in TEST or args[3] == 'все':
                    hw = 'можно удалять!'
                    await Inline.delete.set()
                else:
                    hw = 'подгруппа введена неверно!'
            else:
                hw = 'предмет название подгруппа'
        else:
            hw = 'предмет введен неверно!'
    else:
        pass

    input_content = InputTextMessageContent(hw)
    result_id = '1'
    item = InlineQueryResultArticle(
        title='del_hw:',
        id=result_id,
        description=f'{hw!r}',
        input_message_content=input_content,
    )
    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)