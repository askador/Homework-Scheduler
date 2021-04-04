from bot.loader import dp
from bot.scheduler import scheduler
from aiogram.dispatcher import filters, FSMContext
from bot.states import AddChat
from aiogram import types


@dp.callback_query_handler(lambda c: c.data == 'none', state=AddChat.subgroups)
async def no_subgroups(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['chat_subgroups'] = []

    await callback_query.answer()
