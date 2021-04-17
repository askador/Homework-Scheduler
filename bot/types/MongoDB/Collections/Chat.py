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
        "students",
        "notify",
        "notification_time",
        "emoji_on",
        "photo_mode",
        "can_pin",
        "pin_message_id",
        "homeworks",
    ]

    def __init__(self, _id):
        self.id = int(_id)

    async def add(self, *,
                  title,
                  admins,
                  subjects=[],
                  subgroups=[],
                  students=[],
                  notify=True,
                  notification_time=12,
                  emoji_on=True,
                  photo_mode=True,
                  can_pin=True,
                  pin_message_id=0,
                  homeworks=[]):
        """
        Add new chat
        :param str title: chat title
        :param list admins: list of chat admins
        :param list subjects: list of subjects
        :param list subgroups: subgroups
        :param list students: students id of group
        :param bool notify: to notify chat about deadlines
        :param int notification_time: to do homework notification time
        :param bool emoji_on: can use emoji
        :param bool photo_mode: show homework as a photo
        :param bool can_pin: pin homeworks to do at notification time
        :param int pin_message_id: last pinned bot message
        :param list homeworks: homeworks
        :return changes
        """

        chat = {
            "_id": self.id,
            "title": title,
            "admins": admins,
            "subjects": subjects,
            "subgroups": subgroups,
            "students": students,
            "notify": notify,
            "notification_time": notification_time,
            "emoji_on": emoji_on,
            "photo_mode": photo_mode,
            "can_pin": can_pin,
            "pin_message_id": pin_message_id,
            "homeworks": homeworks
        }

        db = Database()
        return await db.insert(self.__collection_name__, chat)

    async def update(self, *,
                     title=None,
                     admins=None,
                     subjects=None,
                     subgroups=None,
                     students=None,
                     notify=None,
                     notification_time=None,
                     emoji_on=None,
                     photo_mode=None,
                     can_pin=None,
                     pin_message_id=None,
                     ):
        """
        Update chat info
        :param str title: chat title
        :param list admins: chat admins
        :param list subjects: subjects
        :param dict subgroups: subgroups
        :param list students: students id of group
        :param bool notify: to notify chat about deadlines
        :param int notification_time: to do homework notification hour
        :param bool emoji_on: can use emoji
        :param bool photo_mode: show homework as a photo
        :param bool can_pin: pin homeworks to do at notification time
        :param int pin_message_id: last pinned bot message
        :return changes
        """

        fields = {
            "title": title,
            "admins": admins,
            "subjects": subjects,
            "subgroups": subgroups,
            "students": students,
            "notify": notify,
            "notification_time": notification_time,
            "emoji_on": emoji_on,
            "photo_mode": photo_mode,
            "can_pin": can_pin,
            "pin_message_id": pin_message_id,
        }

        db = Database()

        for field, val in fields.items():
            if val is not None:
                await db.update(self.__collection_name__,
                                filters={"_id": self.id},
                                changes={"$set": {f"{field}": val}})

    async def add_hw(self, *,
                     subject,
                     name,
                     description,
                     deadline,
                     subgroup=None,
                     priority='common'
                     ):
        """
        Add homework
        :param str subject: subject
        :param str name: name
        :param str description: description
        :param datetime.datetime deadline: deadline
        :param str subgroup: subgroup id
        :param str priority: work priority
        :return changes
        """

        db = Database()

        last_id = await db.aggregate(self.__collection_name__, [
            {"$unwind": "$homeworks"},
            {"$sort": {"homeworks._id": -1}},
            {"$limit": 1},
            {"$group": {"_id": "$homeworks._id"}}
        ])

        hw = Homework(chat_id=self.id, _id=last_id[0]["_id"])
        return await hw.create(
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
        :param str subgroup: subgroup id
        :param str priority: work priority
        :return changes
        """

        hw = Homework(chat_id=self.id, _id=int(_id))
        await hw.update(
            collection=self.__collection_name__,
            subject=subject,
            subgroup=subgroup,
            name=name,
            description=description,
            deadline=deadline,
            priority=priority)

    async def get_homeworks(self, _id=None, filters: List[Dict] = None, full_info=True, custom_query=None):
        """
        Get homeworks either by id or by list of dates or other filters
        :param int _id: homework id
        :param filters: list of filters
        :param bool full_info:
        :param list custom_query:
        :return list data: homeworks
        """
        data = []
        hw = Homework(chat_id=self.id)

        if custom_query:
            return await hw.get_info(self.__collection_name__,
                                     filters={},
                                     full_info=full_info,
                                     custom_query=custom_query)
        if _id:
            filters = [{'homeworks._id': int(_id)}]
        for _filter in filters:
            return await hw.get_info(self.__collection_name__,
                                     filters=_filter,
                                     full_info=full_info,
                                     custom_query=custom_query)

    async def homeworks_search(self, args, full_info=True):
        """
        Search homeworks by args

        :param list args: search will be implemented by given args
        :param bool full_info:

        :return list data: searched homeworks
        """

        data = []
        hw = Homework(chat_id=self.id)

        fields = [
            'homeworks.subject',
            'homeworks.subgroup',
            'homeworks.name',
            'homeworks.description',
            'format_date_point',
            'format_date_slash'
        ]

        priority = {
            "common": "обычное",
            "important": "важное"
        }

        _and = {}

        if args:
            _and = {"$and": []}

            index = 0
            for arg in args:
                _and['$and'].append({"$or": []})
                for field in fields:
                    _and["$and"][index]["$or"].append(
                        {
                            field: {
                                "$regex": f'{arg}+', "$options": "i"
                            }
                        }
                    )

                for k, v in priority.items():
                    if arg in v:
                        _and["$and"][index]["$or"].append(
                            {
                                'homeworks.priority': {
                                    "$regex": f'{k}', "$options": "i"
                                }
                            }
                        )

                index += 1

        query = [
            {"$match": {"_id": -1001424619068}},
            {"$unwind": "$homeworks"},
            {
                "$addFields": {
                    "format_date_point": {
                        "$dateToString": {"format": "%Y.%m.%d %H.%M", "date": "$homeworks.deadline"},
                    },
                    "format_date_slash": {
                        "$dateToString": {"format": "%Y/%m/%d %H/%M", "date": "$homeworks.deadline"},
                    }
                }
            },
            {"$match": _and},
        ]

        return await hw.get_info(self.__collection_name__,
                                 filters={},
                                 full_info=full_info,
                                 custom_query=query)

    async def delete_hw(self, _id):
        """
        Delete homework
        :param int _id: homework id
        :return changes
        """
        hw = Homework(chat_id=self.id, _id=int(_id))
        return await hw.delete(self.__collection_name__)

    async def get_field_value(self, field):
        db = Database()
        data = await db.find(collection=self.__collection_name__,
                             filters={"_id": self.id},
                             projection={"_id": 0, field: 1})
        data = [d[field] for d in data]
        if not data:
            return []
        return data[0]
