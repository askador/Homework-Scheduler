from bot.loader import dp, bot
import datetime
import asyncio

CHATS = [
    -1001424619068
]

PINS = {

}


async def get_hw(date):
    return "Лаба на часик"


async def remove_hw(date):
    print('removed some hw')


async def show_daily_hw():
    async def each_chat(chat):
        try:
            await bot.unpin_chat_message(chat, PINS[chat])
        except Exception as e:
            pass
        await remove_hw(datetime.datetime.now())
        message = await bot.send_message(chat, await get_hw(datetime.datetime.now()))
        await bot.pin_chat_message(chat, message.message_id)
        PINS[chat] = message.message_id
    cor = [each_chat(chat) for chat in CHATS]
    await asyncio.gather(*cor)
