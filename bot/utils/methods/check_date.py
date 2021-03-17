from time import strptime


async def check_date(date):
    try:
        strptime(date, '%d/%m')
        return True
    except Exception as e:
        try:
            strptime(date, '%d.%m')
            return True
        except Exception as e:
            return False