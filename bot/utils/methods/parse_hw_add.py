from bot.loader import dp
import datetime


async def add_parse_hw(args):

    HW = {}

    HW['subj'] = args[1]
    HW['name'] = args[2]
    HW['subg'] = args[3]
    HW['deadline'] = args[4]
    if len(args) > 5:
        s = ' '
        s = s.join(args[5:])
        if s.find('приоритет:важное') != -1:
            s = s.replace('приоритет:важное', '')
            HW['priority'] = 'important'
        elif s.find('приоритет:обычное') != -1:
            s = s.replace('приоритет:обычное', '')
            HW['priority'] = 'common'
        else:
            HW['priority'] = 'common'
        HW['description'] = s
    else:
        HW['priority'] = 'common'
        HW['description'] = 'name says all for it'

    return HW
