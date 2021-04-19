from bot.types import Database


async def user_in_chat_students(user_id):
    db = Database()

    chat_id = await db.find(collection="chat",
                  filters={"students": {"$eq": int(user_id)}},
                  projection={"_id": 1}
                  )
    if chat_id:
        chat_id = chat_id[0]['_id']
    return chat_id
