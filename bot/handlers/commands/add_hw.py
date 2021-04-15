from bot.data.commands.add_hw import COMMANDS_TEXT, COMMANDS

from bot.loader import dp, bot
from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from bot.keyboards import list_keyboard
from bot.states import SetHomework
from bot.utils.methods import update_last, check_date, make_datetime
from bot.types.MongoDB.Collections import Chat


@dp.message_handler(commands=COMMANDS,  access_level='moderator')
@dp.message_handler(Command(commands=COMMANDS_TEXT, prefixes="!"),  access_level='moderator')
async def add_hw(message: types.Message):
    """
    try:
        arguments = message.get_args().split()
    except Exception as e:
        arguments = None

    SUBJECTS = await Chat(message.chat.id).get_field_value("subjects")

    text = "Выберите предмет или введите его:"

    if arguments is not None and len(arguments) >= 3:
        if arguments[0] in SUBJECTS and await check_date(arguments[2]):
            return await message.reply("все сразу, круто")
        else:
            text = "Введенные данные не подходят, вызываю стандартный диалог.\nВыберите предмет или введите его:"
    elif arguments is None:
        arguments = message.text.split()
        if len(arguments) > 2 and arguments[2] in SUBJECTS and await check_date(arguments[4]):
            return await message.reply("все сразу, круто")
        else:
            text = "Введенные данные не подходят, вызываю стандартный диалог.\nВыберите предмет или введите его:"
    """
    text = "Выберите предмет или введите его:"

    await SetHomework.subject.set()
    state = dp.get_current().current_state()
    await state.update_data(page=1)

    markup = await list_keyboard(message.chat.id, 'subject', 1)
    await update_last(state, await message.reply(text, reply_markup=markup))


@dp.message_handler(Text(startswith="add_hw"), lambda m: m.via_bot)
async def inline_add(message: types.Message):
    # await message.reply("Принял")
    data = message.text.replace("add_hw", "").replace(" ", "").split(",")
    await bot.send_message(message.chat.id, "Задание успешно добавлено!\n\n"
                                                           "<b>Предмет</b>: <i>{}</i>\n"
                                                           "<b>Название</b>: <i>{}</i>\n"
                                                           "<b>Подгруппа</b>: <i>{}</i>\n"
                                                           "<b>Срок сдачи</b>: <i>{}</i>\n"
                                                           "<b>Описание</b>: <i>{}</i>\n"
                                                           "<b>Приоритет</b>: <i>{}</i>".format(
        data[0],
        data[1],
        data[2],
        data[3],
        data[4],
        data[5]), )

    chat = Chat(message.chat.id)
    await chat.add_hw(subject=data[0],
                      subgroup=data[1],
                      name=data[2],
                      description=data[4],
                      deadline=await make_datetime([data[3]]),
                      priority=data[5])



