from utils.types.PosrtgreSQL.Tables.Column import Column
from utils.types.PosrtgreSQL.Tables.ChatHomework import ChatHomework
from utils.types.PosrtgreSQL.Database import Database


class Chat:
    """
    Make convenient interaction with chats

    """

    __tablename__ = "chat"

    columns = {
        'chat_id': Column("chat_id", "bigint", primary_key=True, not_null=True),
        'title': Column("title", "varchar(64)"),
        'admins': Column("admins", "text", not_null=True),
        'subjects': Column("subjects", "text")
    }

    async def create_table(self):
        """
        Create table
        """
        table = f"create table if not exists {self.__tablename__} ("

        for i, col in self.columns.items():
            table += f"{col},"

        table += ")"

        await Database().query(table)

    async def add_chat(self, chat_id, title, admins):
        """
        Add new chat

        :param int chat_id: chat id
        :param str title: chat title
        :param list admins: list of chat admins
        """
        query = f"INSERT INTO {self.__tablename__} (chat_id, title, admins)" \
                f"VALUES ({chat_id}, '{title}', '{admins}')" \
                f"ON CONFLICT (chat_id) DO UPDATE SET title = '{title}'"

        await Database().query(query)

        hw = ChatHomework(chat_id)
        await hw.create_table()

    async def _add_columns(self):
        """
        Add self.columns to table
        """
        db = Database()
        await db.add_column(self.__tablename__, columns=self.columns)


