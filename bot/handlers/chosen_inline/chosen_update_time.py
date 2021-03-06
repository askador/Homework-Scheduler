from bot.loader import dp, bot
from aiogram.types import ChosenInlineResult
from bot.utils.methods import add_parse_hw
from bot.states import InlineSettings
from aiogram.dispatcher import FSMContext


@dp.chosen_inline_handler(lambda chosen_inline_query: True, state=InlineSettings.update_time)
async def chosen_update_time(chosen_inline_query: ChosenInlineResult, state: FSMContext):
    # print(chosen_inline_query.query.split()[2])
    # print(chosen_inline_query.query)

    await state.finish()
