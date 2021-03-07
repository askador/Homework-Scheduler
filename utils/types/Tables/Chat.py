from data.config import token, db_url
import asyncpg
import asyncio

from utils.types.Tables.Column import Column

from pprint import pprint


# class Database:
#
#     def __init__(self):
#         self.db_url = db_url
#
#     async def connect(self):
#         self.conn = await asyncpg.connect(self.db_url)
#
#     def create_table(self, name, args):
#         sql = f"create table {name} if not exists(" \
#               f")"


class Chat:
    __tablename__ = "chat"

    chat_id = Column("chat_id", "bigint", unsigned=True, primary_key=True, not_null=True)
    title = Column("chat_id", "varchar(64)")
    admins = Column("chat_id", "text", not_null=True)

    def __init__(self):
        pass

    async def create_table(self):
        pass

print(Chat.__dict__)