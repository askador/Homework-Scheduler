from aiogram.utils.exceptions import BadRequest, MessageTextIsEmpty, ChatNotFound

from bot.loader import bot
import datetime
from datetime import timedelta
import asyncio
from bot.types import Database
from bot.types.MongoDB import Chat


async def get_hw(chat_id, current_day):
    text = ""
    tomorrow_text = "<b>Завтра нужно сдать</b>\n"
    after_tomorrow_text = "<b>Послезавтра нужно сдать</b>\n"

    tomorrow_day_start = (current_day + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow_day_end = (current_day + timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=59)
    after_tomorrow_day_start = (current_day + timedelta(days=2)).replace(hour=0, minute=0, second=0, microsecond=0)
    after_tomorrow_day_end = (current_day + timedelta(days=2)).replace(hour=23, minute=59, second=59, microsecond=0)

    chat = Chat(chat_id)
    homeworks_tomorrow = await chat.get_homeworks(filters=[
        {
            "$and": [
                {
                    "homeworks.deadline": {
                        "$gte": tomorrow_day_start
                    }
                },
                {
                    "homeworks.deadline": {
                        "$lte": tomorrow_day_end
                    }
                }
            ]
        }
    ])

    homeworks_after_tomorrow = await chat.get_homeworks(filters=[
        {
            "$and": [
                {
                    "homeworks.deadline": {
                        "$gte": after_tomorrow_day_start
                    }
                },
                {
                    "homeworks.deadline": {
                        "$lte": after_tomorrow_day_end
                    }
                }
            ]
        }
    ])

    hws_array = [homeworks_tomorrow, homeworks_after_tomorrow]

    temp_day = 1

    for day in hws_array:
        index = 1

        if day:
            if temp_day == 1:
                text += tomorrow_text
            else:
                text += after_tomorrow_text
            temp_day += 1
            for hw in day:
                hw = hw['_id']
                del hw['_id']
                del hw['deadline']
                del hw['priority']
                subj = hw['subject']
                if hw['subgroup'] != "any":
                    subj += f"{hw['subgroup']}пг."

                text += f"{index}. <b>предмет:</b> {subj}\n" \
                             f"    <b>название:</b> {hw['name']}\n" \
                             f"    <b>описание:</b> {hw['description']}\n\n"

    return text


async def remove_hw(chat_id, date):

    chat = Chat(chat_id)

    homeworks_to_remove = await chat.get_homeworks(filters=[
        {
            "homeworks.deadline": {
                "$lte": date
            }
        }
    ])

    for hw in homeworks_to_remove:
        hw_id = hw['_id']['_id']
        await chat.delete_hw(hw_id)


async def each_chat(chat):
    try:
        if isinstance(chat["pin_message_id"], int):
            await bot.unpin_chat_message(chat["_id"], chat["pin_message_id"])
    except BadRequest:
        print(f"Cannot unpin message {chat['pin_message_id']} in {chat['_id']}")

    await remove_hw(chat["_id"], datetime.datetime.now())
    if chat['notify']:
        try:
            message = await bot.send_message(chat["_id"], await get_hw(chat['_id'], datetime.datetime.now()))
        except MessageTextIsEmpty:
            pass
        except ChatNotFound:
            pass
        else:
            if chat["can_pin"]:
                try:
                    await bot.pin_chat_message(chat["_id"], message.message_id)
                except BadRequest:
                    print(f"Cannot pin message {message.message_id} in {chat['_id']}")

                update_chat_pin_message = Chat(chat['_id'])
                await update_chat_pin_message.update(pin_message_id=message.message_id)


async def show_daily_hw(time):

    db = Database()
    data = await db.find('chat',
                         filters={"notification_time": time},
                         projection={"_id": 1, "pin_message_id": 1, "can_pin": 1, "notify": 1})

    cor = [each_chat(chat) for chat in data]
    await asyncio.gather(*cor)
