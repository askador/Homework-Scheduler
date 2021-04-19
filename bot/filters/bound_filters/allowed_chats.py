from bot.loader import dp, bot
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery, InlineQuery
from typing import Union
from aiogram.types import ChatType


class ChatFilter(BoundFilter):
    key = 'allowed_chats'
    required = True
    default = [ChatType.GROUP, ChatType.SUPERGROUP]

    def __init__(self, allowed_chats):
        self.allowed_chats = allowed_chats

    async def check(self, obj: Union[Message, CallbackQuery, InlineQuery], args=None):
        try:
            if isinstance(obj, Message):
                obj = obj.chat
            elif isinstance(obj, CallbackQuery):
                obj = obj.message.chat
            elif isinstance(obj, InlineQuery):
                return True
            return obj.type in self.allowed_chats
        except AttributeError:
            pass


dp.filters_factory.bind(ChatFilter)
