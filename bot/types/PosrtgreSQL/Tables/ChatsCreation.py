from bot.types.PosrtgreSQL.Tables.Column import Column
from bot.types.PosrtgreSQL.Database import Database


class ChatsCreation:
    """
    Make convenient interaction with chats

    """

    __tablename__ = "chats_creation"

    columns = {
        'chat_id': Column("chat_id", "bigint", primary_key=True, not_null=True),
        'set_subjects_state': Column("set_subjects_state", "bool", default="False"),
        'set_subgroups_state': Column("set_subgroups_state", "bool", default="False"),
    }

    async def create_table(self):
        """
        Create table
        """
        table = f"""create table if not exists {self.__tablename__} ("""

        for i, col in self.columns.items():
            table += f"{col},"

        table += ")"

        await Database().query(table)