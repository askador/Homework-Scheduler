from bot.types.MongoDB.Database import Database
from bot.types.MongoDB.Collections.Homework import Homework


class Chat:
    """
    Make convenient interaction with chats

    {
        "_id": int,
        "title": str,
        "admins": [int, int],
        "subjects": [str, str],
        "subgroups": {
                subj_name: {
                    _id: [name: str, name: str]
                }
            }
        "homeworks": {
                "subject": str,
                "description": str,
                "deadline": datetime,
                "subgroup": int,
            }
    }
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

    def add_chat(self, *, chat_id, title, admins, subjects=None, subgroups=None, homeworks=None):
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

        Database().insert(self.__collection_name__, chat)

    def update_chat(self, *, title, admins=None, subjects=None, subgroups=None):
        """
        Update chat info

        :param str title: chat title
        :param list admins: chat admins
        :param list subjects: subjects
        :param dict subgroups: subgroups
        """

        fields = {
            "title": title,
            "admins": admins,
            "subjects": subjects,
            "subgroups": subgroups,
        }

        db = Database()

        for field, val in fields.items():
            if val:
                db.update(self.__collection_name__,
                          filters={"_id": self.chat_id},
                          changes={"$set": {f"{field}": f"{val}"}})

    def add_hw(self, *,
               subject,
               name,
               description,
               deadline,
               subgroup=None
               ):
        """
        Add homework

        :param str subject: subject
        :param str name: name
        :param str description: description
        :param datetime.datetime deadline: deadline
        :param int subgroup: subgroup id
        """

        last_id = Database().get_sorted(self.__collection_name__, direction=-1, limit=1)

        hw = Homework(chat_id=self.chat_id, id=last_id,)\
            .create(
            subject=subject,
            name=name,
            description=description,
            deadline=deadline,
            subgroup=subgroup)

        Database().update(self.__collection_name__,
                          filters={"_id": self.chat_id},
                          changes={"$push": {"homeworks": hw}})

    def update_hw(self, *,
                  id,
                  subject=None,
                  name=None,
                  description=None,
                  deadline=None,
                  subgroup=None):
        """
        Change homework

        :param int id: homework id
        :param str subject: subject
        :param str name: name
        :param str description: description
        :param datetime.datetime deadline: deadline
        :param int subgroup: subgroup id
        """

        hw = Homework(chat_id=self.chat_id, id=id)
        hw.update(subject=subject,
                  description=description,
                  deadline=deadline,
                  subgroup=subgroup)

    def get_hws(self, id, amount):
        hw = Database().get(self.__collection_name__, filters={[{"_id": self.chat_id}, {""}]})
        pass

    def delete_hw(self, id):
        """
        Delete homework

        :param int id: homework id
        """
        hw = Homework(chat_id=self.chat_id, id=id)
        hw.delete()


