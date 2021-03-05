import psycopg2
# from data.misc import conn, cur
from datetime import datetime, timedelta


class db:

    def __init__(self, name):
        self.name = name


    def create_table(self):
        cur.execute(
            f"CREATE TABLE if not exists {self.name}"
            f"(Id        Serial,"
            f"subject        TEXT          NOT NULL,"
            f"type           VARCHAR(20)     NOT NULL,"
            f"deadline       bigint            NOT NULL,"
            "PRIMARY KEY(Id))")

        conn.commit()


    def add_hw(self, subject, type, deadline):
        pass

    def del_hw(self, subject=None, type=None, deadline=None, all=None):
        pass

    def get_hw(self, date):
        pass

    def is_in(self, subject, type):
        pass
