from bot.loader import dp
from aiogram.dispatcher import filters


@dp.message_handler(filters.IsReplyFilter(is_reply=True), filters.Text(equals="get id"), state='*')
async def get_user_id(msg):
    try:
        await msg.reply(msg.reply_to_message.from_user.id)
    except Exception:
        pass
