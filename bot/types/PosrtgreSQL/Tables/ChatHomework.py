from bot.types.PosrtgreSQL.Tables.Column import Column
from bot.types.PosrtgreSQL.Database import Database


class ChatHomework:
    """
    Make convenient interaction with homework
    """

    __tablename__ = "hw_chat_"

    columns = {
        'id': Column("id", "", serial=True, primary_key=True),
        'subject': Column("subject", "varchar(64)"),
        'description': Column("description", "text", not_null=True),
        'deadline': Column("deadline", "timestamp with time zone",
                           not_null=True,
                           default="now() + interval '1 day'"),
        'subgroup': Column("subgroup", "int")
    }

    def __init__(self, chat_id):
        self.__tablename__ += str(chat_id)

    async def create_table(self):
        """
        Create table
        """
        table = f"""create table if not exists "{self.__tablename__}"  ("""

        for i, col in self.columns.items():
            table += f"{col},"

        table = table[:-1]
        table += ");"

        print(table)

        await Database().query(table)

    async def _add_columns(self):
        """
        Add self.columns to table
        """
        db = Database()
        await db.add_column(self.__tablename__, columns=self.columns)

    async def add_hw(self, *, subject, description, deadline, subgroup='NULL'):
        """
        Add homework

        :param str subject: subject
        :param str description: description
        :param datetime deadline: deadline
        :param int subgroup: subgroup id
        """
        db = Database()

        query = f"""INSERT INTO "{self.__tablename__}" """ \
                f"(subject, description, deadline, subgroup) " \
                f"VALUES ('{subject}', '{description}', '{deadline}', {subgroup})"

        await db.query(query)

        # try:
        #     await db.query(query)
        # except asyncpg.exceptions.UndefinedColumnError as e:
        #     print("Undefined column:", e)
        # except NameError as e:
        #     print(e)
        # except asyncpg.exceptions.PostgresSyntaxError as e:
        #     print("Syntax error:", e)
        # except asyncpg.exceptions.UndefinedTableError as e:
        #     print("Undefined table:", e)

    async def del_hw(self, id):
        """
        Delete homework

        :param int id: homework id
        """
        db = Database()

        query = f"""DELETE FROM "{self.__tablename__}" WHERE id = {id}"""

        await db.query(query)

    async def get_hw(self, id):
        pass


