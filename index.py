from data.config import token, db_url
import asyncpg
import asyncio

from utils.types.Database import Database
from utils.types.Tables.Chat import Chat
from utils.types.Tables.ChatHomework import ChatHomework

from pprint import pprint


async def main():
    # await chat.create_table()
    # await chat.add_chat(1232, "1231asdfas23", "sadf$sdf$dfdf$")

    # data = await db.fetch("SELECT * FROM chat")
    # pprint(data)
    hw = ChatHomework(123)
    await hw.create_table()

    db = Database()
    # sql = f"create table if not exists hw_chat_123  " \
    #       f"(id serial primary key ," \
    #       f"subject varchar(64) ," \
    #       f"description text not null ," \
    #       f"deadline timestamp with time zone not null default(CURRENT_TIMESTAMP));"

    # sql = "DROP TABLE hw_chat_123"
    # sql = "create table if not exists hw_chat_123  (id serial primary key  ,subject varchar(64) ,description text not null ,deadline DATETIME not null default(CURRENT_TIMESTAMP));"

    # await db.query(sql)
    cols = await db._get_table_columns(hw.__tablename__)
    pprint(cols)

asyncio.get_event_loop().run_until_complete(main())
