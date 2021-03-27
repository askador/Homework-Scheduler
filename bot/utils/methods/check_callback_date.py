import datetime


async def check_callback_date(date):
    return date.year >= datetime.datetime.now().year and date.month >= datetime.datetime.now().month \
           and date.day >= datetime.datetime.now().day
