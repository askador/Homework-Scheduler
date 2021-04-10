from bot.loader import dp, bot
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery
from typing import Union
from bot.types.MongoDB.Collections import Chat


class AccessLevelFilter(BoundFilter):
    key = 'access_level'

    def __init__(self, access_level):
        self.access_level = access_level

    async def check(self, obj: Union[Message, CallbackQuery]):
        try:
            if isinstance(obj, Message):
                obj = obj
            elif isinstance(obj, CallbackQuery):
                obj = obj.message
            return obj.type in self.access_level
        except AttributeError:
            pass
        member = await bot.get_chat_member(obj.chat.id, obj.from_user.id)
        if obj.from_user.is_bot:
            return False
        if self.access_level == 'creator':
            return member.is_chat_creator()
        elif self.access_level == 'admin':
            return member.is_chat_admin()
        elif self.access_level == 'moderator':
            chat = Chat(obj.chat.id)
            MODERATORS = await chat.get_field_value('admins')
            return member.is_chat_admin() or obj.from_user.id in MODERATORS
        elif self.access_level == 'member':
            return member.is_chat_member()


dp.filters_factory.bind(AccessLevelFilter)

