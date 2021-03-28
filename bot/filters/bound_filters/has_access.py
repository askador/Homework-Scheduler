from bot.loader import dp, bot
from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

MODERATORS = [
    '1'
]


class MyFilter(BoundFilter):
    key = 'has_access'

    def __init__(self, has_access):
        self.has_access = has_access

    async def check(self, message: types.Message):
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin() or member in MODERATORS


dp.filters_factory.bind(MyFilter)