import asyncpg
from data.config import db_url
from datetime import datetime, timedelta





class Database:

    def __init__(self):
        self.db_url = db_url

    async def connect(self):
        self.conn = await asyncpg.connect(self.db_url)

    def create_table(self):
        pass

    def add_hw(self, subject, type, deadline):
        pass

    def del_hw(self, subject=None, type=None, deadline=None, all=None):
        pass

    def get_hw(self, date):
        pass

    def is_in(self, subject, type):
        pass
