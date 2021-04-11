from bot.data.commands.add_hw import COMMANDS as add_, COMMANDS_TEXT as add_text
from bot.data.commands.del_hw import COMMANDS as del_, COMMANDS_TEXT as del_text
from bot.data.commands.edit_hw import COMMANDS as edit_, COMMANDS_TEXT as edit_text
from bot.data.commands.show_hw import COMMANDS as show_, COMMANDS_TEXT as show_text

from bot.loader import dp
from aiogram.types import ChatType
from aiogram.dispatcher.filters import Command


COMMANDS = add_ + del_ + edit_ + show_
COMMANDS_TEXT = add_text + del_text + edit_text + show_text


@dp.message_handler(Command(commands=COMMANDS_TEXT, prefixes="!"), allowed_chats=[ChatType.PRIVATE])
@dp.message_handler(commands=COMMANDS, allowed_chats=[ChatType.PRIVATE])
async def for_private_commands(msg):
    text = \
"""
Бот предназначен только для общих чатов.

Добавь в свой чат, нажав на ссылку: https://t.me/itai_hw_bot?startgroup=a
"""

    await msg.answer(text)
