import calendar
import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def calendar_keyboard(y, m):
    now = datetime.datetime.now()
    year = now.year + y
    month = now.month + m

    markup = InlineKeyboardMarkup(row_width=7)

    markup.row(InlineKeyboardButton(calendar.month_name[month]+" "+str(year), callback_data='ignore'))

    markup.row()
    for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
        markup.insert(InlineKeyboardButton(day, callback_data='ignore'))


    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        markup.row()
        for day in week:
            if day == 0:
                markup.insert(InlineKeyboardButton(" ", callback_data='ignore'))
            else:
                #row.append(InlineKeyboardButton(str(day), callback_data=['selected', year, month, day]))
                markup.insert(InlineKeyboardButton(str(day), callback_data='selected'))


    markup.row(InlineKeyboardButton('Следующий месяц >>>', callback_data='month'))
    markup.row(InlineKeyboardButton('Следующий год >>>', callback_data='year'))

    #print(markup)
    return markup
