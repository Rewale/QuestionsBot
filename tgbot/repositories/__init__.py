import datetime
from abc import ABC, abstractmethod

from tgbot.models.dto import User, Question, Message, UserInfo
from tgbot.models.role import UserRole


class UserRepo(ABC):
    @abstractmethod
    async def get_user(self, tg_id: int) -> User:
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
    async def get_info(self, phone: str) -> UserInfo:
        pass


class JobTitleRepo(ABC):
    @abstractmethod
    async def submit_job_title(self, job_title: str) -> UserRole:
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
    async def create_message(self, message: Message) -> Message:
        pass

    @abstractmethod
    async def edit_message(self, message: Message, text: str) -> Message:
        pass


class MarkRepo(ABC):
    @abstractmethod
    async def set_mark(self, helpfully: bool, question: Question):
        pass


class Repo:
    def __init__(self, message_repo: MessagesRepo,
                 mark_repo: MarkRepo,
                 question_repo: QuestionRepo,
                 user_repo: UserRepo,
                 user_info_repo: UserInfoRepo,
                 job_title: JobTitleRepo):
        self.mark = mark_repo
        self.message = message_repo
        self.question_repo = question_repo
        self.job_title = job_title
        self.user = user_repo
        self.user_info = user_info_repo
