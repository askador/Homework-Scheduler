from utils.types.MongoDB.Database import Database


class ChatHomework:
    """
    Make convenient interaction with homework
    """

    __collection_name__ = "hw_chat_"

    columns = [
        "_id",
        "subject",
        "description",
        "deadline",
        "subgroup",
    ]

    def __init__(self, chat_id):
        self.__collection_name__ += str(chat_id)

    def create_collection(self):
        null_hw = {}

        for col in self.columns:
            null_hw[col] = None

        db = Database()

        db.insert_one(self.__collection_name__, null_hw)

    def add_hw(self, *, subject, description, deadline, subgroup='NULL'):
        """
        Add homework

        :param str subject: subject
        :param str description: description
        :param datetime deadline: deadline
        :param int subgroup: subgroup id
        """

        hw = {
            "_id": self._increment(),
            "subject": subject,
            "description": description,
            "deadline": deadline,
            "subgroup": subgroup,
        }

        Database().insert_one(self.__collection_name__, hw)

    def _increment(self):
        db = Database()

        last_id = db.get_sorted(self.__collection_name__, direction=-1, limit=1)

        for row in last_id:
            if not isinstance(row["_id"], int):
                return 1

            return row['_id'] + 1

    def del_hw(self, id):
        """
        Delete homework

        :param int id: homework id
        """

        Database().delete_one(self.__collection_name__, filters={"_id": id})



