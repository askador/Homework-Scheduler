from utils.types.PosrtgreSQL.Tables import Column
from utils.types.PosrtgreSQL.Database import Database


class ChatSubgroups:
    """
    Make convenient interaction with subgroups
    """

    __tablename__ = "subgrps_chat_"

    columns = {
        'id': Column("id", "", serial=True, primary_key=True),
        'title': Column("title", "VARCHAR(64)", default="NULL"),
        'uids': Column("uids", "text"),
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

        await Database().query(table)

    async def _add_columns(self):
        """
        Add self.columns to table
        """
        db = Database()
        await db.add_column(self.__tablename__, columns=self.columns)

    async def add_subgroup(self, uids):
        """
        Add new chat subgroup

        :param list uids: subgroup users ids
        """