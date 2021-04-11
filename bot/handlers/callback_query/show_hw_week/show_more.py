from datetime import datetime

from bot.loader import dp

from bot.states import ShowHw
from bot.types.MongoDB import Chat


@dp.callback_query_handler(lambda c: c.data.isdigit(), state=ShowHw.week)
async def show_more(callback_query, state):
    chat = Chat(callback_query.message.chat.id)
    hw = await chat.get_homeworks(_id=callback_query.data, full_info=True)
    hw = hw[0]["_id"]
    await callback_query.message.delete()
    text = ''

    prior = {
        "important": "важное",
        "common": "обычное"
    }

    subg = hw['subgroup']
    if subg == "any":
        subg = 'Все'

    text += f"<b>Предмет:</b> {hw['subject']}\n" \
            f"<b>Подгруппа:</b> {subg}\n" \
            f"<b>Название:</b> {hw['name']}\n" \
            f"<b>Описание:</b> {hw['description']}\n" \
            f"<b>Срок сдачи:</b> {datetime.strftime(hw['deadline'], '%d.%m.%Y %H:%M')}\n" \
            f"<b>Важность:</b> {prior[hw['priority']]}"

    await callback_query.message.answer(text)

    await state.finish()
