from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def generate_hws_kb(homeworks):
    hws_kb = InlineKeyboardMarkup(row_width=1)

    index = 1

    for hw in homeworks:
        hw = hw['_id']
        button_text = f"{index}. {hw['subject']} "

        if hw['subgroup'] != '':
            button_text += f"{hw['subgroup']}пг. "

        button_text += f"{hw['name']}"

        button = InlineKeyboardButton(text=button_text,
                                      callback_data=f"edit_hw {hw['_id']}")

        hws_kb.add(button)

        index += 1

    return hws_kb
