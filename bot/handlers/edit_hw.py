from bot.loader import dp
from aiogram.dispatcher import filters
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import subjects_keyboard

ALIAS = [
    "изменить дз",
    "обновить дз"
]

@dp.message_handler(filters.Text(startswith=ALIAS), is_chat_admin=True)
async def edit_hw(message):
    if (message.text == "регулярОчка"):
        return await message.reply("все сразу, круто")
    else:
        markup = await subjects_keyboard(['peepeepoopoo', 'poopoo'])
        return await message.reply("Выберите предмет или введите его:", reply_markup=markup)