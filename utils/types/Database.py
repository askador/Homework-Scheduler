import asyncpg
from data.config import db_url


class Database:

    def __init__(self):
        self.db_url = db_url

    async def connect(self):
        self.conn = await asyncpg.connect(self.db_url)

    async def close(self):
        await self.conn.close()

    async def create_table(self, table):
        await self.connect()
        # print(query)
        await self.conn.execute(table)
        await self.close()

    async def query(self, query):
        await self.connect()
        await self.conn.execute(query)
        await self.close()

    async def fetch(self, query):
        await self.connect()
        data = await self.conn.fetch(query)
        await self.close()

        return data

    def add_hw(self, subject, type, deadline):
        pass

    def del_hw(self, subject=None, type=None, deadline=None, all=None):
        pass

    def get_hw(self, date):
        pass

    def is_in(self, subject, type):
        pass
