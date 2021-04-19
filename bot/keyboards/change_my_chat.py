from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

change_my_chat_kb = InlineKeyboardMarkup()
change_my_chat_kb.add(InlineKeyboardButton('Сменить чат', callback_data='change_my_chat'))