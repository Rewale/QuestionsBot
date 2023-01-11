from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from tgbot.models.role import UserRole


@dataclass
class UserInfo:
    name: str
    surname: str
    patronymic: str | None
    subdivision: str
    job_title: str


@dataclass
class User(UserInfo):
    id: str | int | None
    role: UserRole
    leader: User | None
    telegram_id: int
    blocked: bool = False


@dataclass
class Question:
    id: str | int | None
    text: str
    created_at: datetime
    close_at: Optional[datetime, None]


@dataclass
class Mark:
    id: str | int | None
    comment: str | None
    helpfully: bool
    question: Question


@dataclass
class Message:
    id: str | int
    text: str
    user: User
    at: datetime
    original_message: Optional[Message, None] = None

    @property
    def original(self) -> bool:
        return self.original_message is None
