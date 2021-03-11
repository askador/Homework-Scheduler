from bot.types.MongoDB.Database import Database
from bot.types.MongoDB.Collections.Homework import Homework


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

    def add_chat(self, *, chat_id, title, admins, subjects, subgroups=None, homeworks=None):
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

    def update_chat(self, *, title, admins=None, subjects=None, subgroups=None):
        """
        Update chat info

        :param str title: chat title
        :param list admins: chat admins
        :param list subjects: subjects
        :param dict subgroups: subgroups
        """

        if admins is None:
            admins = Database().get(self.__collection_name__, {"_id": self.chat_id})['admins']
        if subjects is None:
            subjects = Database().get(self.__collection_name__, {"_id": self.chat_id})['subjects']
        if subgroups is None:
            subgroups = Database().get(self.__collection_name__, {"_id": self.chat_id})['subgroups']

        Database().update(self.__collection_name__, {"_id": self.chat_id}, {"$set": {
                                                                                        "title": title,
                                                                                        "admins": admins,
                                                                                        "subjects": subjects,
                                                                                        "subgroups": subgroups
                                                                                    }
                                                                            })

    def add_hw(self, *,
               subject,
               description,
               deadline,
               subgroup=None):
        """
        Add homework

        :param str subject: subject
        :param str description: description
        :param datetime deadline: deadline
        :param int subgroup: subgroup id
        """

        last_id = Database().get_sorted(self.__collection_name__, direction=-1, limit=1)

        hw = Homework(chat_id=self.chat_id,
                      id=last_id,
                      subject=subject,
                      description=description,
                      deadline=deadline,
                      subgroup=subgroup)

        print(vars(hw))

        hw.add()

    def get_hw(self, id):
        hw = Database().get(self.__collection_name__, filters={[{"_id": self.chat_id}, {""}]})
        pass

    def update_hw(self, id):
        pass

    def delete_hw(self, id):
        pass
