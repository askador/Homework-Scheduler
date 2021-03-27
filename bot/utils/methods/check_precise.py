import datetime


async def check_precise(date, time):
    try:
        time = datetime.datetime.strptime(time, '%H:%M')
        date = date.replace(hour=time.hour)
        date = date.replace(minute=time.minute)

        return date > datetime.datetime.now()
    except Exception as e:
        return False