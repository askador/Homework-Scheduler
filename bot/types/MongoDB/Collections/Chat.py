from typing import List, Dict

from bot.types.MongoDB.Database import Database
from bot.types.MongoDB.Collections.Homework import Homework
from datetime import time


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
        "photo_mode"
        "can_pin",
        "homeworks",
    ]

    def __init__(self, chat_id):
        self.chat_id = chat_id

    async def add_chat(self, *,
                       chat_id,
                       title,
                       admins,
                       subjects=[],
                       subgroups=[],
                       notification_time=time(hour=12, minute=0),
                       emoji_on=True,
                       photo_mode=True,
                       can_pin=True,
                       homeworks=None):
        """
        Add new chat

        :param int chat_id: chat id
        :param str title: chat title
        :param list admins: list of chat admins
        :param list subjects: list of subjects
        :param list subgroups: subgroups
        :param datetime.time notification_time: do homework notification
        :param bool emoji_on: can use emoji
        :param bool photo_mode: show homework as a photo
        :param bool can_pin: pin homeworks to do at notification time
        :param list homeworks: homeworks

        :return changes
        """

        if homeworks is None:
            homeworks = []
        chat = {
            "_id": chat_id,
            "title": title,
            "admins": admins,
            "subjects": subjects,
            "subgroups": subgroups,
            "notification_time": notification_time,
            "emoji_on": emoji_on,
            "photo_mode": photo_mode,
            "can_pin": can_pin,
            "homeworks": homeworks
        }

        db = Database()
        return await db.insert(self.__collection_name__, chat)

    async def update_chat(self, *,
                          title,
                          admins=None,
                          subjects=None,
                          subgroups=None,
                          notification_time=None,
                          emoji_on=None,
                          photo_mode=None,
                          can_pin=None,
                          ):
        """
        Update chat info

        :param str title: chat title
        :param list admins: chat admins
        :param list subjects: subjects
        :param dict subgroups: subgroups
        :param datetime.time notification_time: do homework notification
        :param bool emoji_on:
        :param bool photo_mode:
        :param bool can_pin:
        :return changes
        """

        fields = {
            "title": title,
            "admins": admins,
            "subjects": subjects,
            "subgroups": subgroups,
            "notification_time": notification_time,
            "emoji_on": emoji_on,
            "photo_mode": photo_mode,
            "can_pin": can_pin,
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
                     name,
                     description,
                     deadline,
                     subgroup=None,
                     priority=0
                     ):
        """
        Add homework

        :param str subject: subject
        :param str name: name
        :param str description: description
        :param datetime.datetime deadline: deadline
        :param int subgroup: subgroup id
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

        hw = Homework(chat_id=self.chat_id, id=last_id[0]["_id"])
        return await hw.create(
            collection=self.__collection_name__,
            subject=subject,
            subgroup=subgroup,
            name=name,
            description=description,
            deadline=deadline,
            priority=priority)

    async def update_hw(self, *,
                        id,
                        subject=None,
                        name=None,
                        description=None,
                        deadline=None,
                        subgroup=None,
                        priority=None):
        """
        Change homework

        :param int id: homework id
        :param str subject: subject
        :param str name: name
        :param str description: description
        :param datetime.datetime deadline: deadline
        :param int subgroup: subgroup id
        :param int priority: work priority

        :return changes
        """

        hw = Homework(chat_id=self.chat_id, id=id)
        return await hw.update(
            collection=self.__collection_name__,
            subject=subject,
            subgroup=subgroup,
            name=name,
            description=description,
            deadline=deadline,
            priority=priority)

    async def get_homeworks(self, id=None, filters: List[Dict] = None, full_info=False):
        """
        Get homeworks either by id or by list of dates or other filters

        :param int id: homework id
        :param filters: list of filters
        :param bool full_info:

        :return list data: homeworks
        """
        data = []
        hw = Homework(chat_id=self.chat_id)

        if id:
            filters = [{'homeworks._id': id}]
        for _filter in filters:
            if full_info:
                data = await hw.get_brief_info(self.__collection_name__, filters=_filter)
            else:
                data = await hw.get_full_info(self.__collection_name__, filters=_filter)

        return data

    async def delete_hw(self, id):
        """
        Delete homework

        :param int id: homework id

        :return changes
        """
        hw = Homework(chat_id=self.chat_id, id=id)
        return await hw.delete(self.__collection_name__)

    async def get_field_value(self, field):
        db = Database()

        return await db.find(collection=self.__collection_name__,
                             filters={"_id": self.chat_id},
                             projection={"_id": 0, field: 1})
