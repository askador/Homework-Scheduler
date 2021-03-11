from bot.types.MongoDB.Database import Database


class Homework:
    """
    Make convenient interaction with homework
    """

    columns = [
        "id",
        "subject",
        "description",
        "deadline",
        "subgroup",
    ]

    def __init__(self, *, chat_id=None, id, subject, description, deadline, subgroup):
        self.chat_id = chat_id
        self.id = id
        self.subject = subject
        self.description = description
        self.deadline = deadline
        self.subgroup = subgroup

    @staticmethod
    def _increment(id):
        """
        Increment id

        :param int id: last homework id
        :return int id: incremented id
        """

        if not isinstance(id, int):
            return 1

        return id + 1

    def add(self):
        # TODO: rewrite db query
        """
        Add homework
        """

        hw = {
            "_id": self._increment(self.id),
            "subject": self.subject,
            "description": self.description,
            "deadline": self.deadline,
            "subgroup": self.subgroup,
        }

        Database().client["chat"].update_one({"_id": self.chat_id}, {"$push": {"homeworks": hw}})

    def update(self, *, subject=None, description=None, deadline=None, subgroup=None):
        """
        Update homework info

        :param str subject: subject
        :param str description: description
        :param datetime deadline: deadline
        :param int subgroup: subgroup

        """

        pass

    def delete(self, id):
        """
        Delete homework

        :param int id: homework id
        """

        # Database().delete_one(self.__collection_name__, filters={"_id": id})

    def get(self, id):
        """
        Get homework info

        :param int id: homework id
        :return dict hw: homework info
        """

    # def __repr__(self):
    #     hw = "{'id': 1}"
    #     return hw

