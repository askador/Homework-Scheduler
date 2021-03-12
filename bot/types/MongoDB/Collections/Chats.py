from bot.types.MongoDB.Database import Database


class Chats:
    """
    Make convenient interaction with chats
    """

    __collection_name__ = "chats"

    columns = [
      "_id",
      "title",
      "admins",
      "subjects",
    ]

    def create_collection(self):
        """
        Create collection
        """

        if self.__collection_name__ in Database().client.list_collection_names():
            return False

        null_chat = {}

        for col in self.columns:
            null_chat[col] = None

        db = Database()

        db.insert_one(self.__collection_name__, null_chat)

    def add_chat(self, *, chat_id, title, admins, subjects):
        """
        Add new chat

        :param int chat_id: chat id
        :param str title: chat title
        :param list admins: list of chat admins
        :param list subjects: list of subjects
        """

        chat = {
            "_id": chat_id,
            "title": title,
            "admins": admins,
            "subjects": subjects,
        }

        Database().insert_one(self.__collection_name__, chat)

    def update_chat(self, *, title, admins, subjects):
        """
        Update chat info

        :param str title: chat title
        :param list admins: chat admins
        :param list subjects: subjects
        """

        pass

