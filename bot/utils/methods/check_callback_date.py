import datetime


async def check_callback_date(date):
    return date >= datetime.datetime.now()