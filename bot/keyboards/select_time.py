from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def select_time_keyboard():
    markup = InlineKeyboardMarkup()

    markup.row(InlineKeyboardButton('00:00', callback_data='0'),
               InlineKeyboardButton('01:00', callback_data='1'),
               InlineKeyboardButton('02:00', callback_data='2'),
               InlineKeyboardButton('03:00', callback_data='3'),)

    markup.row(InlineKeyboardButton('04:00', callback_data='4'),
               InlineKeyboardButton('05:00', callback_data='5'),
               InlineKeyboardButton('06:00', callback_data='6'),
               InlineKeyboardButton('07:00', callback_data='7'), )

    markup.row(InlineKeyboardButton('08:00', callback_data='8'),
               InlineKeyboardButton('09:00', callback_data='9'),
               InlineKeyboardButton('10:00', callback_data='10'),
               InlineKeyboardButton('11:00', callback_data='11'), )

    markup.row(InlineKeyboardButton('12:00', callback_data='12'),
               InlineKeyboardButton('13:00', callback_data='13'),
               InlineKeyboardButton('14:00', callback_data='14'),
               InlineKeyboardButton('15:00', callback_data='15'), )

    markup.row(InlineKeyboardButton('16:00', callback_data='16'),
               InlineKeyboardButton('17:00', callback_data='17'),
               InlineKeyboardButton('18:00', callback_data='18'),
               InlineKeyboardButton('19:00', callback_data='19'), )

    markup.row(InlineKeyboardButton('20:00', callback_data='20'),
               InlineKeyboardButton('21:00', callback_data='21'),
               InlineKeyboardButton('22:00', callback_data='22'),
               InlineKeyboardButton('23:00', callback_data='23'), )
    return markup
