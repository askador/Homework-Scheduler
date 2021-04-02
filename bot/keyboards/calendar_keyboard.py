import calendar
import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

Months = ['', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']


async def calendar_keyboard(m):
    now = datetime.datetime.now()
    year = now.year + (now.month + m)//12

    if (now.month + m%12)%12 == 0:
        month = 12
    else:
        month = (now.month + m%12)%12

    markup = InlineKeyboardMarkup(row_width=7)

    markup.row(InlineKeyboardButton(Months[month]+" "+str(year), callback_data='ignore'))

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
                date_time = str(datetime.date(year, month, day))
                markup.insert(InlineKeyboardButton(str(day), callback_data='selected ' + date_time))

    markup.row()
    if m > 0:
        markup.insert(InlineKeyboardButton('⬅️ Предыдущий месяц', callback_data='prev_month'))
    markup.insert(InlineKeyboardButton('Следующий месяц  ➡️', callback_data='next_month'))

    markup.row()
    if m//12 > 0:
        markup.insert(InlineKeyboardButton('⬅️ Предыдущий год', callback_data='prev_year'))
    markup.insert(InlineKeyboardButton('Следующий год  ➡️', callback_data='next_year'))

    #print(markup)
    return markup
