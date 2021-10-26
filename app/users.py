from aiogram import types
from db import users
from exceptions import DoesNotExist
from typing import Optional, NamedTuple, List


class User(NamedTuple):
    id: int
    first_name: str
    last_name: str
    username: Optional[str]
    command_lock: Optional[str]


class UserManager:
    @staticmethod
    def add(user: types.User):
        data = dict(user)
        data['_id'] = data.get('id')
        users.insert_one(data)

    @staticmethod
    def get(query: dict) -> User:
        if instance := users.find_one(query):
            return User(
                id=instance['_id'],
                first_name=instance.get('first_name'),
                last_name=instance.get('last_name'),
                username=instance.get('username'),
                command_lock=instance.get('command_lock'),
            )
        raise DoesNotExist('Send /start to start conversation')

    @staticmethod
    def get_ids() -> List[int]:
        return users.find({}, {'_id': 1})

    @staticmethod
    def lock_command(_id, command):
        users.update_one({'_id': _id}, {'$set': {'command_lock': command}})

    @staticmethod
    def unlock_command(_id):
        users.update_one({'_id': _id}, {'$set': {'command_lock': None}})
