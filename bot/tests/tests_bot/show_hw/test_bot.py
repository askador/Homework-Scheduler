import logging

from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from bot.loader import bot, dp

pinned = []


@dp.message_handler(Text(equals="пин"), user_id=526497876, state='*')
async def add_chat(msg):
    chat_id = -1001424619068

    pinned.append(msg.message_id)

    a = await bot.pin_chat_message(chat_id, msg.message_id)
    print(a)


@dp.message_handler(Text(equals="-пин"), user_id=526497876, state='*')
async def add_chat(msg):
    global pinned
    chat_id = -1001424619068
    a = await bot.unpin_chat_message(chat_id, pinned[-1]+3)
    print(a)
    # del pinned[-1]

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(
        dp, skip_updates=True
    )
