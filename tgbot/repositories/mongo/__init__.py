import datetime
import functools
from abc import ABC
from typing import Callable

from motor.motor_asyncio import AsyncIOMotorDatabase

from tgbot.models.dto import Message, User, Question
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
    def wrapper(*args, **kwargs):
        user = func(*args, **kwargs)
        user['id'] = user['_id']
        del user['_id']
        return User(**user)

    return wrapper


class UserMongoRepo(UserRepo, MongoRepo):
    def __init__(self, db: AsyncIOMotorDatabase, collection_name="users"):
        super().__init__(db, collection_name)

    @return_user
    async def get_user(self, fio: str) -> User:
        user = await self.collection.find_one({'fio': fio})
        user['id'] = user['_id']
        del user['_id']
        return User(**user)

    async def block_user(self, fio: str):
        await self.collection.update_one({{'fio': fio}, {'$set': {'blocked', True}}})

    async def block_user_by_tg(self, tg_id: int):
        await self.collection.update_one({{'telegram_id': tg_id}, {'$set': {'blocked', True}}})

    async def create_user(self, user: User) -> User:
        mongo_id = await self.collection.insert_one(user.__dict__)['_id']
        if not user.id:
            user.id = mongo_id
        return user


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
