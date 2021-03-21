from bot.loader import dp, bot

from aiogram.dispatcher.filters import Command


@dp.message_handler(commands=['help'], state='*')
async def command_help(message):
    help_message = \
"""
Бот для упрощения работы с распорядком домашних заданий студентов

Основные команды:
/help - это сообщение
/add_hw - добавить домашнее задание
/edit_hw - изменить домашнее задание
/del_hw - удалить домашнее задание
/show_hw, !п, !показать дз - показать список домашних заданий
/cancel - сбросить настройку

"""

    await message.answer(help_message)

