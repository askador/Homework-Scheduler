import logging
import re
from aiogram import Bot,Dispatcher, executor, types
from data.config import token

from pprint import pprint


logging.basicConfig(level=logging.INFO)

bot = Bot(token = token)
dp = Dispatcher(bot)


"""
Выбор одного из предметов
"""

async def subject(n, id):
    pass

"""
Быстрый вывод дз неделю
"""
async def fast_hw(id):
    pass

"""
Установить напоминание: отдельное задание, отдельный предмет или постоянно
За 24 часа
"""
async def remind(id):
    pass


@dp.message_handler(lambda msg: msg.text.lower() == "админы")
async def mes(msg):
    admins_object = await bot.get_chat_administrators(msg.chat.id)

    admins_list = []

    for admin in admins_object:
        admins_list.append(admin.user.id)


@dp.message_handler(lambda msg: msg.reply_to_message is not None and msg.text.lower() == "getid")
async def get_id(msg):
    try:
        await msg.reply(msg.reply_to_message.from_user.id)
    except Exception:
        pass

# @dp.message_handler(lambda msg: re.findall("\Aдобавить дз" ,msg.text.lower()))
# async def add_hw(message):
#     await c_add_hw(message)
#
# @dp.message_handler(lambda msg: msg.text.lower() == "показать дз")
# async def echo(message):
#     await c_get_hw(message)
#
# @dp.message_handler(lambda msg: msg.text.lower() == "справка")
# async def info(message):
#     await c_info(message)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)