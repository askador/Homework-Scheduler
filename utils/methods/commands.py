import sys
from datetime import datetime, timedelta
sys.path.append('D:/dz_bot')
import data.config 
# from data.misc import conn, cur, sh_subjects
# from utils.types.db import db
# from aiogram import types
# from data.config import admins


# db = db('test5')

def validate(func):
    async def wrapper(message):
        try:
            s = message.text.split()
            datetime.strptime(s[4], '%d.%m.%Y')
            if(s[2] in sh_subjects):
                return await func(message)
            else:
                return await message.reply("Неверные аргументы. Правильная структура: добавить дз <предмет> <задание> <дата дд.мм.гггг.ЧЧ:ММ>",reply = False)
        except ValueError:
            return await message.reply("Неверные аргументы. Правильная структура: добавить дз <предмет> <задание> <дата дд.мм.гггг.ЧЧ:ММ>",reply = False)
    return wrapper

def readable(arr):
    s = ''
    for i in arr:
        s+=str(i[0]) + ' ' + str(i[1]) + ' ' + datetime.fromtimestamp(int(i[2])).strftime('%d.%m.%Y.%H:%M') +'\n'
    return s

@validate
async def c_add_hw(message):
    s = message.text.split()
    if len(db.is_in(s[2],s[3])) == 0:
        db.add_hw(s[2], s[3], int(datetime.strptime(s[4], '%d.%m.%Y.%H:%M').timestamp()))
        return await message.reply('Успешно добавлено', reply = False)
    else:
        return await message.reply('Уже внесено в базу данных', reply = False)
    

async def c_get_hw(message):
    date = datetime.now() + timedelta(days=7)
    return await message.reply(readable(db.get_hw(int(date.timestamp()))),reply = False)

async def c_info(message):
    return await message.reply("Список комманд:\n"
    "добавить дз <предмет> <задание> <дата дд.мм.гггг.ЧЧ:ММ> - предложить дз администратору или добавить его если вы администратор\n"
    "показать дз - домашка на ближайшую неделю, можно также проверить следующие недели\n"
     ,reply = False)

def admin(func):
    async def wrapper(message):
        if message['from']['id'] in admins:
            return await func(message)
        else:
            return await message.reply("Недостаточно прав",reply = False) 
    return wrapper       


#c_add_hw('добавить дз апр лаб3 17.11.2020 14:00')
