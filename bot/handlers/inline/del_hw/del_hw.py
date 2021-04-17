from datetime import datetime
from bot.loader import dp, bot
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from aiogram.dispatcher import filters, FSMContext
from bot.states import Inline
from bot.types.MongoDB import Chat
from bot.utils.methods import user_in_chat_students
from bot.types.MongoDB import Chat


@dp.inline_handler(filters.Text(startswith=['del_hw']))
async def inline_del_hw(inline_query: InlineQuery, state: FSMContext):
    args = inline_query.query.split()[1:]

    chat_id = await user_in_chat_students(inline_query.from_user.id)
    if not chat_id:
        await inline_query.answer(results=[
            InlineQueryResultArticle(
                title='Показать дз',
                id='1',
                description='Вы не привязаны к группе!\n'
                            'Воспользуйтесь ботом в чате, куда вы хотите получать ответ',
                input_message_content=InputTextMessageContent(
                    message_text='Вы не привязаны к группе!\n'
                                 'Воспользуйтесь ботом в чате, куда вы хотите получать ответ'
                )
            )
        ],
            cache_time=0)
        return
    chat = Chat(chat_id)

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
                input_message_content=InputTextMessageContent(message_text=message_text),
                thumb_url="https://i.imgur.com/DV2Wwcm.png", thumb_height=32, thumb_width=32
            )

            results.append(article)

    results = results[:50]

    await inline_query.answer(results=results, cache_time=0)