from bot.loader import dp, bot
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from aiogram.dispatcher import filters, FSMContext
from bot.utils.methods import check_date
from bot.tests.tests_bot.states_test.states_test import Inline
from aiogram.dispatcher.filters.state import State


TEST = [
    "1"
]


@dp.inline_handler(filters.Text(startswith=['add_hw']))
@dp.inline_handler(filters.Text(startswith=['add_hw']), state=Inline.add)
async def inline_add_hw(inline_query: InlineQuery, state: FSMContext):
    # state = dp.get_current().current_state()
    await state.finish()
    print(inline_query)

    args = inline_query.query.split()

    hw = 'loading...'
    item = None

    if len(args) == 1:
        hw = 'предмет название подгруппа срок_сдачи'
    elif len(args) >= 2:
        if args[1] in TEST:
            hw = 'предмет название подгруппа срок_сдачи'
            if len(args) >=4:
                if args[3] in TEST or args[3] == 'все':
                    pass
                else:
                    hw = 'подгруппа введена неверно!'
                if len(args) >= 5:
                    if await check_date([args[4]]):
                        hw = 'успешно заполнено!'
                        await Inline.add.set()
                    else:
                        hw = 'дата введена неверно!'
                else:
                    pass
            else:
                pass
        else:
            hw = 'предмет введен неверно!'
    else:
        pass

    input_content = InputTextMessageContent(hw, parse_mode='HTML')
    result_id = '1'
    item = InlineQueryResultArticle(
        title='add_hw:',
        id=result_id,
        description=f'{hw!r}',
        input_message_content=input_content,
    )

    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)