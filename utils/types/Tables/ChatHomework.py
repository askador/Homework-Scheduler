from utils.types.Tables.Column import Column
from utils.types.Database import Database


class ChatHomework:
    """
    Make convenient interaction with homework
    """

    __tablename__ = "hw_chat_"

    columns = {
        'id': Column("id", "", serial=True, primary_key=True),
        'subject': Column("subject", "varchar(64)"),
        'description': Column("description", "text", not_null=True),
        'deadline': Column("deadline", "timestamp with time zone", not_null=True, default="CURRENT_TIMESTAMP"),
    }

    def __init__(self, chat_id):
        self.__tablename__ += str(chat_id)

    async def create_table(self):
        """
        Create table
        """
        table = f"create table if not exists {self.__tablename__}  ("

        for i, col in self.columns.items():
            table += f"{col},"

        table = table[:-1]
        table += ");"

        await Database().query(table)

    async def _add_columns(self):
        """
        Add self.columns to table
        """
        db = Database()
        await db.add_column(self.__tablename__, columns=self.columns)

    async def add_hw(self, *, subject, description, deadline):
        """
        Add homework

        :param str subject: subject
        :param str description: description
        :param datetime deadline: deadline
        """
        db = Database()

        query = f"INSERT INTO {self.__tablename__}" \
                f"(subject, desciption, deadline) " \
                f"VALUES ('{subject}', '{description}', '{deadline}')"

        await db.query(query)

    async def del_hw(self, id):
        """
        Delete homework

        :param int id: homework id
        """
        db = Database()

        query = f"DELETE FROM {self.__tablename__} WHERE id = {id}"

        await db.query(query)

    async def get_hw(self, id):
        pass


