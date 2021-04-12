from datetime import datetime

from bot.loader import dp, bot
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from aiogram.dispatcher import filters, FSMContext
from bot.utils.methods import check_date
from bot.states import Inline
from bot.types.MongoDB import Chat

users = {
    526497876: -1001424619068
}

COMMANDS = (
    'дз',
    'показать'
)


# TODO inline
#
# if inline_query.query.strip() == "":
#     await inline_query.answer(results=[
#         InlineQueryResultArticle(
#             title='show_hw:',
#             id='1',
#             description='Вы не состоите в группе',
#             input_message_content=InputTextMessageContent(message_text="test")
#         )
#     ],
#         cache_time=0)


@dp.inline_handler(lambda inline_query: inline_query.query.startswith(COMMANDS))
async def show_hw(inline_query: InlineQuery):
    args = inline_query.query.split()[1:]

    chat = Chat(users[int(inline_query.from_user.id)])
    homeworks = sorted(await chat.homeworks_search(args=args, full_info=True), key=lambda x: x["_id"]["_id"])

    results = []

    if not homeworks:
        not_found = InlineQueryResultArticle(
            title="По запросу ничего не нашлось",
            id='0',
            description='',
            input_message_content=InputTextMessageContent(message_text="По запросу ничего не нашлось")
        )
        results.append(not_found)
    else:
        for hw in homeworks:
            hw = hw['_id']

            subg = ''
            if hw['subgroup'] != "any":
                subg = f"{hw['subgroup']}пг."

            title = f"{hw['subject']} {subg} {hw['name']}"
            descr = f"{datetime.strftime(hw['deadline'], '%d.%m.%y')}\n" \
                    f"{hw['description']}"

            message_text = f"<b>Предмет:</b> {hw['subject']}\n" \
                           f"<b>Подгруппа:</b> {subg}\n" \
                           f"<b>Название:</b> {hw['name']}\n" \
                           f"<b>Срок сдачи:</b> {datetime.strftime(hw['deadline'], '%d.%m.%Y %H:%M')}\n" \
                           f"<b>Описание:</b> {hw['description']}\n" \
                           f"<b>Дополнильные материалы:</b> <u>materials</u>\n"

            article = InlineQueryResultArticle(
                title=title,
                id=str(hw['_id']),
                description=descr,
                input_message_content=InputTextMessageContent(message_text=message_text)
            )

            results.append(article)

    results = results[:50]

    await inline_query.answer(results=results, cache_time=0)
