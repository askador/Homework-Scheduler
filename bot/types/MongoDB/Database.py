import pymongo
from bot.data.config import mongodb_setting
from bot.data.config import mongodb_url


class Database:

    def __init__(self, db=None):
        """
        :param str db: optional
        """
        self.user = mongodb_setting['User']
        self.password = mongodb_setting['Password']
        self.host = mongodb_setting['Host']
        self.database = mongodb_setting["Database"] if db is None else db
        self.args = mongodb_setting['args']
        self.mongodb_url = f"mongodb+srv://{self.user}:{self.password}@" \
                           f"{self.host}/{self.database}?{self.args}"

        self.client = pymongo.MongoClient(mongodb_url)

    async def insert(self, collection, document):
        """
        insert document to collection

        :param str collection:
        :param dict document:
        :return bool: if successfully inserted
        """

        return self.client[self.database][collection].insert_one(document)

    async def find(self, collection, filters=None, projection=None):
        """
        Get documents

        :param str collection: collection name
        :param dict filters: filters
        :param dict projection: projection
        :return list data: list of founded documents
        """

        data = list(self.client[self.database][collection].find(filters, projection))

        return data

    async def get_sorted(self, collection, filters=None, sort_by="_id", direction=None, limit=None):
        """
        Get sorted list of collection documents

        :param str collection: collection title
        :param dict filters: filters {"key": "value"}
        :param str sort_by: sort by key
        :param int direction: asc = 1; desc = -1
        :param int limit: documents amount
        :return list sorted docs: list of sorted documents
        """
        sorted_docs = self.client[self.database][collection].find(filters).sort([(sort_by, direction)])

        return sorted_docs.limit(limit)

    async def aggregate(self, collection, pipeline):
        """
        Get aggregated data

        :param str collection: collection
        :param list pipeline: pipeline
        :return list data: list of founded documents
        """

        data = list(self.client[self.database][collection].aggregate(pipeline))

        return data

    async def update(self, collection, filters, changes):
        """
        Update document

        :param str collection: collection
        :param dict filters: filters
        :param dict changes: changes
        """
        return self.client[self.database][collection].update_many(filters, changes)

    async def delete(self, collection, filters=None):
        """
        Delete document

        :param str collection: collection title
        :param dict filters: filters
        """

        return self.client[self.database][collection].delete_many(filters)

    async def count_documents(self, collection):
        """
        Amount of documents in collection

        :param str collection: name of collection
        :return int amount
        """

        return self.client[self.database][collection].count_documents({})
