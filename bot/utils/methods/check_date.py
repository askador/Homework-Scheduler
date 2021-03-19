from time import strptime


async def check_date(date):
    if len(date) == 1:
        print(date)
        try:
            strptime(date[0], '%d/%m')
            return True
        except Exception as e:
            try:
                strptime(date[0], '%d.%m')
                return True
            except Exception as e:
                try:
                    strptime(date[0], '%d/%m/%Y')
                    return True
                except Exception as e:
                    print(e)
                    try:
                        strptime(date[0], '%d.%m.%Y')
                        return True
                    except Exception as e:
                        return False
    if len(date) == 2:
        try:
            strptime(date[0], '%d/%m')
            strptime(date[1], '%H:%M')
            return True
        except Exception as e:
            try:
                strptime(date[0], '%d.%m')
                strptime(date[1], '%H:%M')
                return True
            except Exception as e:
                try:
                    strptime(date[0], '%d/%m/%Y')
                    strptime(date[1], '%H:%M')
                    return True
                except Exception as e:
                    try:
                        strptime(date[0], '%d.%m.%Y')
                        strptime(date[1], '%H:%M')
                        return True
                    except Exception as e:
                        return False
    else:
        return False