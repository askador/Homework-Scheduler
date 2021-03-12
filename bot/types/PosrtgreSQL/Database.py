import asyncpg
from bot.data import postresql_db_url


class Database:
    """
    Make convenient interaction with database
    """

    def __init__(self):
        """
        Set db uri
        """
        self.db_url = postresql_db_url
        self.conn = None

    async def connect(self):
        """
        Connect to db
        """
        self.conn = await asyncpg.connect(self.db_url)

    async def close(self):
        """
        Close connection
        """
        await self.conn.close()

    async def query(self, query):
        """
        Query implementing

        :param str query: query
        """
        await self.connect()
        await self.conn.execute(query)
        await self.close()

    async def fetch(self, query):
        """
        Fetch data

        :param str query: query
        :return str data: Fetched records
        """
        await self.connect()
        data = await self.conn.fetch(query)
        await self.close()

        return data

    async def fetchval(self, query):
        """
        Fetch value of first record

        :param str query: query
        :return str data: Fetched value
        """
        await self.connect()

        val = await self.conn.fetchval(query)
        await self.close()

        return val

    async def copy_table(self, __tablename__, *, columns):
        """
        Fetch value of first record

        :param str __tablename__: tablename
        :return str result: copied rows
        """
        await self.connect()
        result = await self.conn.copy_from_table(
            __tablename__, columns = columns,
            output='file.csv', format='csv'
        )
        await self.close()
        return result

    async def add_column(self, __tablename__, columns):
        """
        Add columns to table

        :param str __tablename__: tablename
        :param dict columns: list of columns to add
        """
        _current_table_last_column_name = await self.fetch(f"select column_name "
                                                           f"from information_schema.columns "
                                                           f"""where table_name = "{__tablename__}" """
                                                        )
        _current_table_last_column_name = _current_table_last_column_name[-1][0]

        cols_to_add = []

        add = False
        for i, col in enumerate(columns):
            if col == _current_table_last_column_name:
                add = True
            if add:
                cols_to_add.append(col)

        if cols_to_add:
            del cols_to_add[0]
            for col in cols_to_add:
                query = f"ALTER TABLE {__tablename__} ADD COLUMN {columns[col]}"
                await self.query(query)

    async def _get_table_columns(self, __tablename__):
        """

        :param str __tablename__: tablename
        :return list columns: list of table columns
        """
        await self.connect()
        query = f"""SELECT column_name FROM information_schema.columns WHERE table_name = "{__tablename__}" """
        columns = await self.conn.fetch(query)
        await self.close()

        return columns

