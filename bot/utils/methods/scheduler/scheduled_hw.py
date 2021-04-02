from bot.loader import dp, bot
import datetime
import asyncio
from bot.types import Database
from aiogram import types

"""
CHATS = [
    -1001424619068
]

PINS = [

]

ALLOWS = [

]
"""


async def get_hw(date):
    return "Лаба на часик"


async def remove_hw(date):
    print('removed some hw')


async def show_daily_hw(time):

    # global CHATS, PINS, ALLOWS
    db = Database()
    data = await db.find('chat', filters={"notification_time": time}, projection={"_id": 1, "pin_message_id": 1,
                                                                                  "can_pin": 1})
    # CHATS = [chat["_id"] for chat in data]
    # PINS = [chat["pin_message_id"] for chat in data]
    # ALLOWS = [chat["can_pin"] for chat in data]
    # print(CHATS)

    async def each_chat(chat):
        try:
            print(chat["pin_message_id"])
            await bot.unpin_chat_message(chat["_id"], chat["pin_message_id"])
        except Exception as e:
            pass
        await remove_hw(datetime.datetime.now())
        message = await bot.send_message(chat["_id"], await get_hw(datetime.datetime.now()))
        if chat["can_pin"]:
            await bot.pin_chat_message(chat["_id"], message.message_id)
        await db.update('chat', filters={"_id": chat["_id"]}, changes={"$set": {"pin_message_id": message.message_id}})
        # PINS[chat] = message.message_id

    cor = [each_chat(chat) for chat in data]
    await asyncio.gather(*cor)
