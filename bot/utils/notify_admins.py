from typing import List, Union
from contextlib import suppress
from aiogram.utils.exceptions import ChatNotFound

from bot.loader import dp


async def notify_admins(admins: Union[List[int], List[str], int, str]):
    for admin in admins:
        with suppress(ChatNotFound):
            await dp.bot.send_message(admin, "Вставай шошлык")
