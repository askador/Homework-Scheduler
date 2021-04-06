from bot.loader import dp, bot
from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from bot.types.MongoDB.Collections import Chat


class AccessLevelFilter(BoundFilter):
    key = 'access_level'

    def __init__(self, access_level):
        self.access_level = access_level

    async def check(self, message: types.Message):
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if message.from_user.is_bot:
            return False
        if self.access_level == 'creator':
            return member.is_chat_creator()
        elif self.access_level == 'admin':
            return member.is_chat_admin()
        elif self.access_level == 'moderator':
            chat = Chat(message.chat.id)
            MODERATORS = await chat.get_field_value('admins')
            return member.is_chat_admin() or message.from_user.id in MODERATORS
        elif self.access_level == 'member':
            return member.is_chat_member()


dp.filters_factory.bind(AccessLevelFilter)

