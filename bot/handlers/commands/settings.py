from bot.loader import dp, bot
from aiogram.dispatcher import filters, FSMContext
from aiogram import types
from bot.keyboards import settings_keyboard
from bot.states import Settings
from bot.utils.methods import update_last
from bot.data.commands.settings import COMMANDS, COMMANDS_TEXT


@dp.message_handler(commands=COMMANDS,  access_level='admin')
@dp.message_handler(filters.Command(commands=COMMANDS_TEXT), access_level='admin')
async def settings(message):
    markup = await settings_keyboard()
    await Settings.choice.set()
    state = dp.get_current().current_state()
    await update_last(state, await message.reply("Открыто меню настроек", reply_markup=markup))


@dp.callback_query_handler(lambda c: c.data == 'back', state=Settings.all_states)
async def back_to_choice(callback_query: types.CallbackQuery, state: FSMContext):
    # await clear(state)
    await Settings.choice.set()
    markup = await settings_keyboard()
    await update_last(state, await bot.edit_message_text("Меню настроек", callback_query.message.chat.id,
                                                         callback_query.message.message_id, reply_markup=markup))


@dp.callback_query_handler(lambda c: c.data == 'done', state=Settings.all_states)
async def back_to_choice(callback_query: types.CallbackQuery, state: FSMContext):
    # await clear(state)
    await state.finish()
    await bot.edit_message_text("Удачно завершено", callback_query.message.chat.id,
                                                         callback_query.message.message_id)