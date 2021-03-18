from time import strptime


async def make_datetime(date):
    try:
        datetime = strptime(date, '%d/%m')
        return datetime
    except Exception as e:
        datetime = strptime(date, '%d.%m')
        return datetime