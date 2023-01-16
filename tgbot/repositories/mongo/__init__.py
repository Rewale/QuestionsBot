import datetime
import functools
from abc import ABC
from copy import copy
from typing import Callable, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from tgbot.models.dto import Message, User, Question
from tgbot.models.role import UserRole
from tgbot.repositories import MessagesRepo, UserRepo, QuestionRepo, MarkRepo


class MongoRepo(ABC):
    def __init__(self, db: AsyncIOMotorDatabase, collection_name):
        self.collection = db.get_collection(collection_name)


class MessagesMongoRepo(MessagesRepo, MongoRepo):

    def __init__(self, db: AsyncIOMotorDatabase, collection_name="messages"):
        super().__init__(db, collection_name)

    async def create_message(self, message: Message) -> Message:
        user = await self.collection.insert_one(message.__dict__)
        return Message(**user)

    async def edit_message(self, message: Message, text: str) -> Message:
        pass


def return_user(func: Callable):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        user = await func(*args, **kwargs)
        user['id'] = user['_id']
        del user['_id']
        return User(**user)

    return wrapper


class UserMongoRepo(UserRepo, MongoRepo):
    def __init__(self, db: AsyncIOMotorDatabase, collection_name="users"):
        super().__init__(db, collection_name)

    async def get_user(self, tg_id: int) -> Optional[User]:
        user = await self.collection.find_one({'telegram_id': tg_id})
        if not user:
            return None
        del user['id']
        del user['_id']
        user['role'] = UserRole(user['role'])
        return User(**user)

    async def block_user(self, fio: str):
        await self.collection.update_one({{'fio': fio}, {'$set': {'blocked', True}}})

    async def block_user_by_tg(self, tg_id: int):
        await self.collection.update_one({{'telegram_id': tg_id}, {'$set': {'blocked', True}}})

    async def create_user(self, user: User):
        insert_dict = copy(user.__dict__)
        insert_dict['role'] = insert_dict['role'].value
        await self.collection.insert_one(insert_dict)


class QuestionMongoRepo(QuestionRepo, MongoRepo):
    def __init__(self, db, collection_name: str = "questions"):
        super().__init__(db, collection_name)

    async def create_question(self, author: User, text: str) -> Question:
        pass

    async def start_answering(self, answerer: User):
        pass

    async def end_answering(self, ender: User):
        pass


class MarkMongoRepo(MarkRepo, MongoRepo):
    def __init__(self, db, collection_name="marks"):
        super().__init__(db, collection_name)

    async def set_mark(self, helpfully: bool, question: Question):
        pass
