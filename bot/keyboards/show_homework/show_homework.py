from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

homework_kb_next_week = InlineKeyboardMarkup(
    row_width=1,
)
homework_kb_next_week.add(
    InlineKeyboardButton(text="Следующая неделя  ➡️", callback_data="next_week"),
    InlineKeyboardButton(text="✖️ Закрыть", callback_data="close")
)

homework_kb_both = InlineKeyboardMarkup(row_width=2)
homework_kb_both.add(
        InlineKeyboardButton(text="⬅️ Предыдущая неделя", callback_data="prev_week"),
        InlineKeyboardButton(text="Следующая неделя  ➡️", callback_data="next_week"),
        InlineKeyboardButton(text="✖️ Закрыть", callback_data="close")
)
