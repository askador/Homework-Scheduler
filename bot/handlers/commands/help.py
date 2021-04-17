from bot.loader import dp, bot
from aiogram.types import ChatType
from bot.utils.methods import bind_student_to_chat


@dp.message_handler(commands=['help'], state='*', allowed_chats=[ChatType.GROUP, ChatType.SUPERGROUP, ChatType.PRIVATE])
async def bot_help(message):

    if message.chat.type != 'private':
        await bind_student_to_chat(message.from_user.id, message.chat.id)

    help_message = \
"""
Чтобы пользоваться функционалом бота добавьте его в группу https://t.me/AI4HWBOT?startgroup=a

<b>Основные команды:</b>
Для всех участников:
/help - это сообщение
/show_hws, !п, !показать дз - показать список домашних заданий
/hw_details, !н, !найти дз - поиск и получение подробной информации по домашнему заданию
/cancel - принудительно завершить работу с командой
/my_chat - показать чат, к котому вы привязаны с возможнностью его смены
 
Для модераторов:
/add_hw, !д, !добавить дз - добавить домашнее задание
/edit_hw, !и !изменить дз - изменить домашнее задание
/del_hw, !у, !удалить дз - удалить домашнее задание

Для администраторов:
/settings - настройка параметров бота

Для основателя группы:
!повысить(в ответ на сообщение) - повышение участника чата до модератора
!понизить(в ответ на сообщение) - исключение участника чата из модераторов

P. S. Если не работает какая то из команд, это означает, что вы не завершили работу с предыдущей командой или стали 
жертвой ошибки. В таком случае, чтобы начать работу с другой командой закройте диалоговое окно прошлой команды,
либо используйте /cancel

Для /show_hws можно использовать аргументы типа показа дз:
- <i>/show_hws текст</i> - показать список домашних заданий текстом
- <i>/show_hws фото</i> - показать список домашних заданий изображением

Так же можно использовать аргументы для быстрого поиска, удаления и изменения домашнего задания:
<i>/hw_details &ltпредмет&gt &ltподгруппа&gt &ltназвание&gt &ltсрок сдачи&gt &ltописание&gt</i>
<i>/del_hw &ltпредмет&gt &ltподгруппа&gt &ltназвание&gt &ltсрок сдачи&gt &ltописание&gt</i>
<i>/edit_hw &ltпредмет&gt &ltподгруппа&gt &ltназвание&gt &ltсрок сдачи&gt &ltописание&gt</i>
<b>Порядок аргументов не важен</b>

<b>Примеры использования:</b>
- <i>!показать математика 01.01.2021</i>
- <i>!изменить химия 2пг</i>
- <i>!у иностранные языки тест 02.02.2021 подгодовиться к тесту по пятой теме</i>

Если хотите использовать функционал напоминания о сроках сдачи с закреплением сообщения, 
пожалуйста, убедитесь, что бот имеет возможность закреплять сообщения.
"""


    await message.answer(help_message)

