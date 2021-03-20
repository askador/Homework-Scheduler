from bot.types.MongoDB.Database import Database


class Homework:
    """
    Make convenient interaction with homework
    """

    columns = [
        "id",
        "subject",
        "name",
        "description",
        "deadline",
        "subgroup",
        "priority",
    ]

    def __init__(self, *, chat_id=None, id):
        self.chat_id = chat_id
        self.id = id

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

    def create(self, *, subject, name, description, deadline, subgroup, priority=0):
        """
        Add homework

        :param str subject:
        :param str name:
        :param str description:
        :param datetime.datetime deadline:
        :param int subgroup:
        :param int priority: priority of work

        :return dict hw: homework data
        """

        hw = {
            "_id": self._increment(self.id),
            "subject": subject,
            "name",
            "description": description,
            "deadline": deadline,
            "subgroup": subgroup,
            "priority": priority,
        }

        return hw

    def update(self, collection, *,
               subject=None,
               name=None,
               description=None,
               deadline=None,
               subgroup=None,
               priority=None):
        """
        Update homework info

        :param str collection: collection
        :param str subject: subject
        :param str name: name
        :param str description: description
        :param datetime.datetime deadline: deadline
        :param int subgroup: subgroup
        :param int priority: work priority

        """

        fields = {
            "subject": subject,
            "name": name,
            "description": description,
            "deadline": deadline,
            "subgroup": subgroup,
            "priority": priority,
        }

        db = Database()

        for field, val in fields.items():
            if val:
                db.update(collection,
                          filters={"_id": self.chat_id, "hws": {"$elemMatch": {"_id": self.id}}},
                          changes={"$set": {f"hws.$.{field}": f"{val}"}})

    def get_short(self):
        """
        Get homework info

        :return dict hw: homework short info
        """

    def get_full(self):
        """
        Get homework info

        :return dict hw: homework full info
        """

    def delete(self, collection):
        """
        Delete homework

        :param collection: collection
        """

        Database().delete(collection,
                          filters={
                              "_id": self.chat_id,
                              "hws": {"$elemMatch": {"_id": self.id}}
                          })

    # def __repr__(self):
    #     hw = "{'id': 1}"
    #     return hw

