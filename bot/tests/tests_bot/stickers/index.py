from aiogram import executor
from bot.tests.tests_bot.loader import dp, bot
import logging
from aiogram.types import ContentType
from aiogram.dispatcher.filters import Text
import time

logging.basicConfig(level=logging.INFO)

ids = []

@dp.message_handler(content_types=[ContentType.STICKER, ContentType.PHOTO, ContentType.DOCUMENT])
async def s(message):
    global ids
    ids.append(message.document.file_id)
    print(ids)

@dp.message_handler(Text(equals="создать"))
async def c(msg):
    await bot.create_new_sticker_set(
        user_id=526497876,
        name="test_stickers_by_ksdgbot",
        title="TestCardsBot",
        emojis="🤪",
        png_sticker=ids[0]
    )
    del ids[0]
    for stick in ids:
        await bot.add_sticker_to_set(
            user_id=526497876,
            name="test_stickers_by_ksdgbot",
            emojis="🤪",
            png_sticker=stick
        )
        await bot.send_sticker()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

