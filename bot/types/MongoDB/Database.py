import pymongo
from bot.data.config import mongodb_url

# ---------- for aiogram-fsm -------------
# start_db_name_index = mongodb_url.rfind("/")
# db_name_indexes = [mongodb_url.rfind("/")+1, mongodb_url.rfind("?")]
# db_name = mongodb_url[mongodb_url.rfind("/")+1:mongodb_url.rfind("?")]
#
# print(db_name)
# print(mongodb_url.replace(db_name, "TEST_DB"))
# print(mongodb_url)
# ----------------------------------------


class Database:

    def __init__(self):
        self.client = pymongo.MongoClient(mongodb_url)

    def insert(self, collection, document):
        """
        insert document to collection

        :param str collection:
        :param dict document:
        :return bool: if successfully inserted
        """

        self.client[collection].insert_one(document)

    def get(self, collection, filters=None, limit=None):

        for doc in self.client[collection].find({filters}):
            return doc

    def get_sorted(self, collection, filters=None, sort_by="_id", direction=None, limit=None):
        """
        Get sorted list of collection documents

        :param str collection: collection title
        :param dict filters: filters {"key": "value"}
        :param str sort_by: sort by key
        :param int direction: asc = 1; desc = -1
        :param int limit: documents amount
        :return list sorted docs: list of sorted documents
        """
        sorted_docs = self.client[collection].find(filters).sort([(sort_by, direction)])

        return sorted_docs.limit(limit)

    def update(self, collection, filters, changes):
        # TODO: rewrite
        """
        Update document

        :param str collection: collection
        :param dict filters: filters
        :param dict changes: changes
        """
        self.client[collection].update_many(filters, changes)

    def delete(self, collection, filters=None):
        """
        Delete document

        :param str collection: collection title
        :param dict filters: filters
        """

        self.client[collection].delete_many(filters)



