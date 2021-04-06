from bot.data.commands.add_hw import COMMANDS as add_
from bot.data.commands.del_hw import COMMANDS as del_
from bot.data.commands.edit_hw import COMMANDS as edit_
from bot.data.commands.show_hw import COMMANDS as show_

from bot.loader import dp
from aiogram.types import ChatType


COMMANDS = add_ + del_ + edit_ + show_


@dp.message_handler(commands=COMMANDS, allowed_chats=[ChatType.PRIVATE])
async def for_private_commands(msg):
    text = \
"""
Бот предназначен только для общих чатов.

Добавь в свой чат, нажав на ссылку: https://t.me/itai_hw_bot?startgroup=a
"""

    await msg.answer(text)
