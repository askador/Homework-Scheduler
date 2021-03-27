from bot.loader import dp
from bot.utils.methods import clear


@dp.message_handler(commands=['cancel'], state='*')
async def cancel(message):
    state = dp.get_current().current_state()
    await clear(state)
    await state.finish()
    await message.reply("Диалог был обнулен")