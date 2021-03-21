from aiogram import types
from bot.data.config import commands


async def set_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand(command, descr) for command, descr in commands.items()
        ]
    )
