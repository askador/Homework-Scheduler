from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from bot.loader import bot
from bot.types import Database
from bot.data.config import MAX_CHATS_AMOUNT


class ChatAmount(BaseMiddleware):
    async def on_pre_process_update(self, update, data):
        a = (await Database().count_documents('chat'))
        if a >= MAX_CHATS_AMOUNT:
            chat_id = False
            if update.message:
                chat_id = update.message.chat.id
            elif update.callback_query:
                chat_id = update.callback_query.message.chat.id
            if chat_id:
                await bot.send_message(chat_id,
                                       "Достигнут лимит групп!")
            raise CancelHandler()
