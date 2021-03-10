import pymongo
from bot.data import mongodb_url

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

    def insert_one(self, collection, document):
        """
        insert document to collection

        :param str collection:
        :param dict document:
        :return bool: if successfully inserted
        """
        # insert_one(document)
        return False

    def insert_many(self, collection, documents):
        # insert_many(documents)
        pass

    def get(self, collection, filters=None):
        # find(filters)
        pass

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

    def update(self, collection, document, change):
        # update_many(document, change)
        pass

    def delete_one(self, collection, filters=None):
        """
        Delete document

        :param str collection: collection title
        :param dict filters: filters {"key": "value"}
        """

        self.client[collection].delete_one(filters)

    def delete_many(self, collection, filters=None):
        # delete_many(filters)
        pass



