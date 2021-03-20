import datetime


async def compare(date):
    return date >= datetime.datetime.now()


async def check_date(date):
    if len(date) == 1:
        try:
            selected = datetime.datetime.strptime(date[0], '%d/%m')
            selected = selected.replace(year=datetime.datetime.now().year)
            return await compare(selected)
        except Exception as e:
            try:
                selected = datetime.datetime.strptime(date[0], '%d.%m')
                selected = selected.replace(year=datetime.datetime.now().year)
                return await compare(selected)
            except Exception as e:
                try:
                    selected = datetime.datetime.strptime(date[0], '%d/%m/%Y')
                    selected = selected.replace(year=datetime.datetime.now().year)
                    return await compare(selected)
                except Exception as e:
                    print(e)
                    try:
                        selected = datetime.datetime.strptime(date[0], '%d.%m.%Y')
                        selected = selected.replace(year=datetime.datetime.now().year)
                        return await compare(selected)
                    except Exception as e:
                        return False
    if len(date) == 2:
        try:
            selected = datetime.datetime.strptime(date[0], '%d/%m')
            selected2 = datetime.datetime.strptime(date[1], '%H:%M')
            selected = selected.replace(hour=selected2.hour, minute=selected2.minute)
            selected = selected.replace(year=datetime.datetime.now().year)
            return await compare(selected)
        except Exception as e:
            try:
                selected = datetime.datetime.strptime(date[0], '%d.%m')
                selected2 = datetime.datetime.strptime(date[1], '%H:%M')
                selected = selected.replace(hour=selected2.hour, minute=selected2.minute)
                selected = selected.replace(year=datetime.datetime.now().year)
                return await compare(selected)
            except Exception as e:
                try:
                    selected = datetime.datetime.strptime(date[0], '%d/%m/%Y')
                    selected2 = datetime.datetime.strptime(date[1], '%H:%M')
                    selected = selected.replace(hour=selected2.hour, minute=selected2.minute)
                    selected = selected.replace(year=datetime.datetime.now().year)
                    return await compare(selected)
                except Exception as e:
                    try:
                        selected = datetime.datetime.strptime(date[0], '%d.%m.%Y')
                        selected2 = datetime.datetime.strptime(date[1], '%H:%M')
                        selected = selected.replace(hour=selected2.hour, minute=selected2.minute)
                        selected = selected.replace(year=datetime.datetime.now().year)
                        return await compare(selected)
                    except Exception as e:
                        return False
    else:
        return False