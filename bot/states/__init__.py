from . import get_public_hw
from aiogram.dispatcher.filters.state import State, StatesGroup


class AddChat(StatesGroup):
    subjects = State()
    subgroups = State()


class SetHomework(StatesGroup):
    subject = State()
    name = State()
    subgroup = State()
    deadline = State()
    deadline_precise = State()
    description = State()
    priority = State()


class GetHomework(StatesGroup):
    homework = State()
    subject = State()
    name = State()
    subgroup = State()
    choice = State()
    deadline = State()
    deadline_precise = State()
    description = State()


class Settings(StatesGroup):
    choice = State()
    subjects = State()
    add_subjects = State()
    subgroups = State()
    add_subgroups = State()
    notifications = State()
    terms = State()
    moderators = State()
    appearance = State()


class DeleteHomework(StatesGroup):
    subject = State()
    name = State()
    subgroup = State()
    homework = State()


class Inline(StatesGroup):
    add = State()
    edit = State()
    delete = State()


class InlineSettings(StatesGroup):
    # choice = State()
    moderators = State()
    notifications = State()
    update_time = State()
    appearance = State()
