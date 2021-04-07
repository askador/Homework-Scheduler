import datetime


async def make_datetime(date):
    if len(date) == 1:
        try:
            date_time = datetime.datetime.strptime(date[0], '%d/%m')
            date_time = date_time.replace(year=datetime.datetime.now().year)
            return date_time
        except Exception as e:
            try:
                date_time = datetime.datetime.strptime(date[0], '%d.%m')
                date_time = date_time.replace(year=datetime.datetime.now().year)
                return date_time
            except Exception as e:
                try:
                    date_time = datetime.datetime.strptime(date[0], '%d/%m/%Y')
                    return date_time
                except Exception as e:
                    date_time = datetime.datetime.strptime(date[0], '%d.%m.%Y')
                    return date_time
    else:
        try:
            date_time = datetime.datetime.strptime(date[0], '%d/%m')
            date_time2 = datetime.datetime.strptime(date[1], '%H:%M')
            date_time = date_time.replace(year=datetime.datetime.now().year)
            date_time = date_time.replace(hour=date_time2.hour, minute=date_time2.minute)
            return date_time
        except Exception as e:
            try:
                date_time = datetime.datetime.strptime(date[0], '%d.%m')
                date_time2 = datetime.datetime.strptime(date[1], '%H:%M')
                date_time = date_time.replace(year=datetime.datetime.now().year)
                date_time = date_time.replace(hour=date_time2.hour, minute=date_time2.minute)
                return date_time
            except Exception as e:
                try:
                    date_time = datetime.datetime.strptime(date[0], '%d/%m/%Y')
                    date_time2 = datetime.datetime.strptime(date[1], '%H:%M')
                    date_time = date_time.replace(hour=date_time2.hour, minute=date_time2.minute)
                    return date_time
                except Exception as e:
                    date_time = datetime.datetime.strptime(date[0], '%d.%m.%Y')
                    date_time2 = datetime.datetime.strptime(date[1], '%H:%M')
                    date_time = date_time.replace(hour=date_time2.hour, minute=date_time2.minute)
                    return date_time


