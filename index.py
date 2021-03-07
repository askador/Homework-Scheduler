from data.config import token, db_url
import asyncpg
import asyncio

from utils.types.Tables.Chat import Chat
from utils.types.Database import Database

from pprint import pprint


async def main():
    chat = Chat()
    await chat.create_table()
    await chat.add_chat(1232, "1231asdfas23", "sadf$sdf$dfdf$")

    db = Database()

    data = await db.fetch("SELECT * FROM chat")

    pprint(data)


asyncio.get_event_loop().run_until_complete(main())
