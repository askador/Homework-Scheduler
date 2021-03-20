from bot.loader import bot

async def show_hw(message):
    await bot.send_message(message.chat.id, 'Пришло дз')
