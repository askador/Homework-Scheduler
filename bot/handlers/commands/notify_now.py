from aiogram.dispatcher.filters import Command
from datetime import datetime

from bot.loader import dp
from bot.data.commands.notify_now import COMMANDS, COMMANDS_TEXT
from bot.utils.methods.scheduler.scheduled_hw import get_hw


@dp.message_handler(Command(commands=COMMANDS), state='*')
@dp.message_handler(Command(commands=COMMANDS_TEXT, prefixes="!"), state='*')
async def notify_now(message):
    text = await get_hw(message.chat.id, datetime.now())
    await message.answer(text)
