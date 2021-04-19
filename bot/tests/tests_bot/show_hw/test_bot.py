import logging

from aiogram.utils import executor
from aiogram.dispatcher.filters import Command
from bot.tests.tests_bot.loader import bot, dp

from bot.keyboards import list_keyboard
from bot.states import GetHomework
from bot.data.commands.edit_hw import COMMANDS, COMMANDS_TEXT
from bot.types.MongoDB.Collections import Chat


@dp.message_handler(Command(commands=COMMANDS_TEXT, prefixes="!"))
@dp.message_handler(Command(commands=COMMANDS, prefixes="/"))
async def edit_hw(message):
    chat_id = message.chat.id
    chat = Chat(chat_id)

    args = message.get_args().split() if message.is_command() else message.text.split()[1:]

    homeworks = sorted(await chat.homeworks_search(args=args, full_info=False), key=lambda x: x["_id"]["_id"])

    if not homeworks:
        await message.reply("По запросу ничего не нашлось")
        return

    kb = await list_keyboard(message.chat.id, 'homework', page=1, arr=homeworks)
    await message.answer(text="дз",
                         reply_markup=kb)

    # await GetHomework.homework.set()
    # state = dp.get_current().current_state()
    # await state.update_data(page=1)
    #
    # kb = await list_keyboard(message.chat.id, 'homework', 1)
    # await message.answer(text="Выберите задание, которое Вы хотите редактировать",
    #                      reply_markup=kb)

    """
    SUBJECTS = await Chat(message.chat.id).get_field_value("subjects")

    try:
        arguments = message.get_args().split()
    except Exception as e:
        arguments = None

    # print(arguments)
    text = "Выберите предмет или введите его:"

    if arguments is not None and len(arguments) >= 2:
        if arguments[0] in SUBJECTS:
            return await message.reply("все сразу, круто")
        else:
            text = "Введенные данные не подходят, вызываю стандартный диалог.\nВыберите предмет или введите его:"
    elif arguments is None:
        arguments = message.text.split()
        if len(arguments) > 2 and arguments[2] in SUBJECTS:
            return await message.reply("все сразу, круто")
        else:
            text = "Введенные данные не подходят, вызываю стандартный диалог.\nВыберите предмет или введите его:"

    await GetHomework.subject.set()
    state = dp.get_current().current_state()
    await state.update_data(page=1)
    markup = await subjects_keyboard(SUBJECTS, 1)
    await update_last(state, await message.reply(text, reply_markup=markup))
    """


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(
        dp, skip_updates=True
    )
