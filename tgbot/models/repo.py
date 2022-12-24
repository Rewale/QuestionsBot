import datetime
from abc import ABC, abstractmethod

from tgbot.models.dto import User, Question, Message


class UserRepo(ABC):
    @abstractmethod
    async def get_user(self, fio: str) -> User:
        pass

    @abstractmethod
    async def block_user(self, fio: str) -> User:
        pass

    @abstractmethod
    async def block_user_by_tg(self, tg_id: int) -> User:
        pass

    @abstractmethod
    async def create_user(self, user: User):
        pass


class UserInfoRepo(ABC):
    @abstractmethod
    async def get_info(self, phone: str) -> User:
        pass


class JobTitleRepo(ABC):
    @abstractmethod
    async def submit_job_title(self, job_title: str) -> bool:
        """ Сравнение должности со списком """
        pass


class QuestionRepo(ABC):
    @abstractmethod
    async def create_question(self, author: User, text: str) -> Question:
        pass

    @abstractmethod
    async def start_answering(self, answerer: User):
        pass

    @abstractmethod
    async def end_answering(self, ender: User):
        """
        @param ender: Тот кто закончил диалог
        """
        pass


class MessagesRepo(ABC):
    @abstractmethod
    async def create_message(self, from_tg_id: int, text: str, question: User, at: datetime.datetime = None) -> Message:
        pass

    @abstractmethod
    async def edit_message(self, message: Message, text: str) -> Message:
        pass


class MarkRepo(ABC):
    @abstractmethod
    async def set_mark(self, helpfully: bool, question: Question):
        pass
