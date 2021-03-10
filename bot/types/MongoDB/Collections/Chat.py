from bot.types.MongoDB.Database import Database


class Chat:
    """
    Make convenient interaction with chats
    """

    __collection_name__ = "chat"

    columns = [
        "_id",
        "title",
        "admins",
        "subjects",
        "subgroups",
        "homeworks",
    ]

    def __init__(self, chat_id):
        self.chat_id = chat_id

    def add_chat(self, *, chat_id, title, admins, subjects, subgroups, homeworks=None):
        """
        Add new chat

        :param int chat_id: chat id
        :param str title: chat title
        :param list admins: list of chat admins
        :param list subjects: list of subjects
        :param dict subgroups: chat subgroups
        :param dict homeworks: homeworks
        """

        chat = {
            "_id": chat_id,
            "title": title,
            "admins": admins,
            "subjects": subjects,
            "subgroups": subgroups,
            "homeworks": homeworks
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

