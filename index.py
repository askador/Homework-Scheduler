from aiogram import Bot, Dispatcher
from data.config import token, db_url
import asyncpg
import asyncio

from pprint import pprint
from aiogram.utils import executor

bot = Bot(token=token)
dp = Dispatcher(bot)



class DB:

    def __init__(self):
        self.db_url = db_url

    async def db_connect(self):
        self.conn = await asyncpg.connect(db_url)

    async def execute(self, sql):
        await self.db_connect()
        await self.conn.execute(sql)

    async def query(self, sql):
        await self.db_connect()
        _data = await self.conn.fetch(sql)
        return _data

    async def val_query(self, sql):
        await self.db_connect()
        _data = await self.conn.fetchval(sql)
        print(_data)

    async def row_query(self, sql):
        await self.db_connect()
        _data = await self.conn.fetchrow(sql)
        print(_data[0])


async def main():
    _db = DB()
    data=await _db.query("SELECT table_schema || '.' || table_name FROM information_schema.tables")
    for table in data:
        try:
            await _db.execute(f"DROP TABLE {table[0]}")
            print(f"DROPPED {table[0]}")
        except Exception:
            print(f"FAILED {table[0]}")
    # await _db.val_query("SELECT * FROM daily_plays")


asyncio.get_event_loop().run_until_complete(main())

"""
SELECT
    table_schema || '.' || table_name
FROM
    information_schema.tables
"""


# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)

