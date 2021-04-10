from bot.types.MongoDB import Database


class Homework:
    """
    Make convenient interaction with homework

    make sure using correct fields sequence
    """

    columns = [
        "id",
        "subject",
        "subgroup",
        "name",
        "description",
        "deadline",
        "priority",
    ]

    def __init__(self, *, chat_id, _id=None):
        self.chat_id = chat_id
        self.id = _id

    @staticmethod
    def _increment(_id):
        """
        Increment id

        :param int _id: last homework id
        :return int id: incremented id
        """

        if not isinstance(_id, int):
            return 1

        return _id + 1

    async def create(self, collection, *, subject, subgroup, name, description, deadline, priority='common'):
        """
        Add homework

        :param str collection: db collection with chat homeworks
        :param str subject:
        :param str subgroup:
        :param str name:
        :param str description:
        :param datetime.datetime deadline:
        :param str priority: priority of work

        :return
            dict if successfully created
            else - 0
        """

        if not isinstance(self.id, int):
            return 0

        hw = {
            "_id": self._increment(self.id),
            "subject": subject,
            "subgroup": subgroup,
            "name": name,
            "description": description,
            "deadline": deadline,
            "priority": priority,
        }

        db = Database()
        return await db.update(collection,
                               filters={"_id": self.chat_id},
                               changes={"$push": {"homeworks": hw}})

    async def update(self, collection, *,
                     subject=None,
                     subgroup=None,
                     name=None,
                     description=None,
                     deadline=None,
                     priority=None):
        """
        Update homework info

        :param str collection: collection
        :param int subgroup: subgroup
        :param str subject: subject
        :param str name: name
        :param str description: description
        :param datetime.datetime deadline: deadline
        :param str priority: work priority

        :return
            dict changes_log if successfully created
            else - 0
        """

        if not isinstance(self.id, int):
            return 0

        fields = {
            "subject": subject,
            "subgroup": subgroup,
            "name": name,
            "description": description,
            "deadline": deadline,
            "priority": priority,
        }

        db = Database()

        for field, val in fields.items():
            if val:
                await db.update(collection,
                                filters={"_id": self.chat_id,
                                         "homeworks": {"$elemMatch": {"_id": self.id}}},
                                changes={"$set": {f"homeworks.$.{field}": val}})

    async def get_info(self, collection, by_id=False, filters=None, full_info=True, custom_query=None):
        """
        Get homework info

        :param str collection:
        :param dict filters: filters
        :param bool by_id: search by hw id
        :param bool full_info: show full hw info
        :param list custom_query: create custom_query

        :return dict brief_info: homework(s) brief info
        """

        group = {
            "_id": {
                "_id": "$homeworks._id",
                "subject": "$homeworks.subject",
                "subgroup": "$homeworks.subgroup",
                "name": "$homeworks.name",
                "priority": "$homeworks.priority",
                "deadline": "$homeworks.deadline"
            }
        }

        db = Database()

        if custom_query:
            return await db.aggregate(collection=collection, pipeline=custom_query)

        if by_id:
            if not isinstance(self.id, int):
                return

            filters = {'homeworks._id': self.id}

        if full_info:
            group["_id"].update([
                ("description", "$homeworks.description"),
            ])

        data = await db.aggregate(collection=collection,
                                  pipeline=[
                                      {"$match": {"_id": self.chat_id}},
                                      {"$unwind": "$homeworks"},
                                      {"$match": filters},
                                      {
                                          "$group": group
                                      },

                                  ])

        return data

    async def delete(self, collection):
        """
        Delete homework

        :param collection: collection

        :return
            dict if successfully deleted
            else - 0
        """

        if not isinstance(self.id, int):
            return 0

        db = Database()
        return await db.update(collection=collection,
                               filters={"_id": self.chat_id},
                               changes={"$pull": {"homeworks": {"_id": self.id}}})

    # def __repr__(self):
    #     hw = "{'id': 1}"
    #     return hw
