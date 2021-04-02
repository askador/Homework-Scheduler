from typing import List, Dict

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
        "notification_time",
        "emoji_on",
        "photo_modo"
        "pin",
        "homeworks",
    ]

    def __init__(self, chat_id):
        self.chat_id = chat_id

    async def add(self, *,
                  title,
                  admins,
                  subjects=None,
                  subgroups=None,
                  notification_time=None,
                  homeworks=None):
        """
        Add new chat

        :param str title: chat title
        :param list admins: list of chat admins
        :param list subjects: list of subjects
        :param dict subgroups: chat subgroups
        :param dict homeworks: homeworks

        :return changes
        """

        chat = {
            "_id": self.chat_id,
            "title": title,
            "admins": admins,
            "subjects": subjects,
            "subgroups": subgroups,
            "homeworks": homeworks
        }

        db = Database()
        return await db.insert(self.__collection_name__, chat)

    async def update(self, *, title, admins=None, subjects=None, subgroups=None):
        """
        Update chat info

        :param str title: chat title
        :param list admins: chat admins
        :param list subjects: subjects
        :param dict subgroups: subgroups

        :return changes
        """

        fields = {
            "title": title,
            "admins": admins,
            "subjects": subjects,
            "subgroups": subgroups,
        }

        db = Database()

        changes_log = []

        for field, val in fields.items():
            if val:
                changes_log.append(await db.update(self.__collection_name__,
                                                   filters={"_id": self.chat_id},
                                                   changes={"$set": {f"{field}": f"{val}"}}))

        return changes_log

    async def add_hw(self, *,
                     subject,
                     subgroup=None,
                     name,
                     description,
                     deadline,
                     priority=0
                     ):
        """
        Add homework

        :param str subject: subject
        :param int subgroup: subgroup id
        :param str name: name
        :param str description: description
        :param datetime.datetime deadline: deadline
        :param int priority: work priority

        :return changes
        """

        db = Database()

        last_id = await db.aggregate(self.__collection_name__, [
            {"$unwind": "$homeworks"},
            {"$sort": {"homeworks._id": -1}},
            {"$limit": 1},
            {"$group": {"_id": "$homeworks._id"}}
        ])

        if last_id:
            last_id = last_id[0]["_id"]
        else:
            last_id = 0

        hw = Homework(chat_id=self.chat_id, id=last_id)
        await hw.create(
            collection=self.__collection_name__,
            subject=subject,
            subgroup=subgroup,
            name=name,
            description=description,
            deadline=deadline,
            priority=priority)

    async def update_hw(self, *,
                        _id,
                        subject=None,
                        name=None,
                        description=None,
                        deadline=None,
                        subgroup=None,
                        priority=None):
        """
        Change homework

        :param int _id: homework id
        :param str subject: subject
        :param str name: name
        :param str description: description
        :param datetime.datetime deadline: deadline
        :param int subgroup: subgroup id
        :param int priority: work priority

        :return changes
        """

        hw = Homework(chat_id=self.chat_id, id=_id)
        return await hw.update(
            collection=self.__collection_name__,
            subject=subject,
            subgroup=subgroup,
            name=name,
            description=description,
            deadline=deadline,
            priority=priority)

    async def get_homeworks(self, _id=None, filters: List[Dict] = None, full_info=False):
        """
        Get homeworks either by id or by list of dates or other filters

        :param int _id: homework id
        :param filters: list of filters
        :param bool full_info:

        :return list data: homeworks
        """
        data = []
        hw = Homework(chat_id=self.chat_id)

        if _id:
            filters = [{'homeworks._id': _id}]
        for _filter in filters:
            if full_info:
                data = await hw.get_brief_info(self.__collection_name__, filters=_filter)
            else:
                data = await hw.get_full_info(self.__collection_name__, filters=_filter)

        return data

    async def get_subjects(self):
        """
        Get list of subjects in this chat
        """

        db = Database()
        data = await db.find(self.__collection_name__, projection={"_id": 0, "subjects": 1})
        return data[0]["subjects"]

    async def get_subgroups(self):
        """
        Get list of subgroups in this chat
        """

        db = Database()
        data = await db.find(self.__collection_name__, projection={"_id": 0, "subgroups": 1})
        return data[0]["subgroups"]

    async def delete_hw(self, _id):
        """
        Delete homework

        :param int _id: homework id

        :return changes
        """
        hw = Homework(chat_id=self.chat_id, id=_id)
        return await hw.delete(self.__collection_name__)

    async def get_field_value(self, field):
        db = Database()

        return await db.find(collection=self.__collection_name__,
                             filters={"_id": self.chat_id},
                             projection={"_id": 0, field: 1})

    async def set_field_value(self, field, value):
        db = Database()

        return await db.update(collection=self.__collection_name__,
                             filters={"_id": self.chat_id},
                             changes={"$set": {field: value}})
