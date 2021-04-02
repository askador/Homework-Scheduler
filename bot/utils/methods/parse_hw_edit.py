from bot.loader import dp
import datetime
from bot.utils.methods import check_date

PRIORITIES = [
    'обычное',
    'важное'
]

HW = {'deadline': '',
      'description': '',
      'priority': 'common'
}


async def edit_parse_hw(hw_string, to_dict):

    args = hw_string

    if args.find('удалить') != -1:
        return 'delete'

    if args.find('срок:') != -1:
        args = args[args.find('срок:'):]
        args = args[args.find(':')+1:]
        if args.find(' ') != -1:
            HW['deadline'] = args[:args.find(' ')+1]
        # print(args)
        if not (await check_date([args])):
            return 'date_error'
        args = hw_string

    if args.find('описание:') != -1:
        args = args[args.find('описание:'):]
        args = args[args.find(':')+1:]
        if args.find(' ') != -1:
            HW['description'] = args[:args.find(' ') + 1]
        # print(args)
        args = hw_string

    if args.find('приоритет:') != -1:
        args = args[args.find('приоритет:'):]
        args = args[args.find(':')+1:]
        if args.find(' ') != -1:
            HW['priority'] = args[:args.find(' ') + 1]
        # print(args)
        if not (args in PRIORITIES):
            return 'prior_error'

    if to_dict == 1:
        return HW
    else:
        return 'ok'


