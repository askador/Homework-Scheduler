from utils.types.Tables.Column import Column
from utils.types.Database import Database


class Chat:
    __tablename__ = "chat"

    chat_id = Column("chat_id", "bigint", primary_key=True, not_null=True)
    title = Column("title", "varchar(64)")
    admins = Column("admins", "text", not_null=True)

    async def create_table(self):
        table = f"create table if not exists {self.__tablename__}  (" \
                f"{self.chat_id}," \
                f"{self.title}," \
                f"{self.admins})"

        await Database().create_table(table)

    async def add_chat(self, chat_id, title, admins):
        query = f"INSERT INTO {self.__tablename__} (chat_id, title, admins)" \
                f"VALUES ({chat_id}, '{title}', '{admins}')" \
                f"ON CONFLICT (chat_id) DO UPDATE SET title = '{title}'"

        await Database().query(query)