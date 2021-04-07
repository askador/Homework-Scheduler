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

    async def create(self, collection, *, subject, subgroup, name, description, deadline, priority=0):
        """
        Add homework

        :param str collection: db collection with chat homeworks
        :param str subject:
        :param int subgroup:
        :param str name:
        :param str description:
        :param datetime.datetime deadline:
        :param int priority: priority of work

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
        :param int priority: work priority

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
                                changes={"$set": {f"homeworks.$.{field}": f"{val}"}})

    async def get_brief_info(self, collection, by_id=False, filters=None):
        """
        Get homework info

        :param str collection:
        :param dict filters: filters
        :param bool by_id: search by hw id

        :return dict brief_info: homework(s) brief info
        """

        db = Database()

        if by_id:
            filters = {'homeworks._id': self.id}

        brief_info = await db.aggregate(collection=collection,
                                        pipeline=[
                                            {"$match": {"_id": self.chat_id}},
                                            {"$unwind": "$homeworks"},
                                            {"$match": filters},
                                            {
                                                "$group": {
                                                    "_id": {
                                                        "_id": "$homeworks._id",
                                                        "subject": "$homeworks.subject",
                                                        "subgroup": "$homeworks.subgroup",
                                                        "name": "$homeworks.name",
                                                        "priority": "$homeworks.priority",
                                                        "deadline": "$homeworks.deadline"
                                                    }
                                                }
                                            },
                                        ]
                                        )

        return brief_info

    async def get_full_info(self, collection, by_id=False, filters=None):
        """
        Get homework info

        :param str collection:
        :param dict filters: filters
        :param bool by_id: search by hw id

        :return dict hw: homework(s) full info
        """

        db = Database()
        if by_id:
            filters = {'homeworks._id': self.id}

        hw = await db.aggregate(collection=collection,
                                pipeline=[
                                    {"$match": {"_id": self.chat_id}},
                                    {"$unwind": "$homeworks"},
                                    {"$match": filters},
                                    {
                                        "$group": {
                                            "_id": {
                                                "_id": "$homeworks._id",
                                                "subject": "$homeworks.subject",
                                                "subgroup": "$homeworks.subgroup",
                                                "name": "$homeworks.name",
                                                "description": "$homeworks.description",
                                                "deadline": "$homeworks.deadline",
                                                "priority": "$homeworks.priority",
                                            }
                                        }
                                    },
                                ]
                                )

        return hw

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
        return await db.delete(collection,
                               filters={
                                   "_id": self.chat_id,
                                   "hws": {"$elemMatch": {"_id": self.id}}
                               })

    # def __repr__(self):
    #     hw = "{'id': 1}"
    #     return hw
