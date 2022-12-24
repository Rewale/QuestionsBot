from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from tgbot.models.role import UserRole


@dataclass
class User:
    role: UserRole
    name: str
    surname: str
    patronymic: str | None
    leader: User | None
    job_title: str
    telegram_id: int
    subdivision: Any
    blocked: bool = False


@dataclass
class Question:
    text: str
    created_at: datetime
    close_at: datetime | None


@dataclass
class Mark:
    comment: str | None
    helpfully: bool
    question: Question


@dataclass
class Message:
    text: str
    user: User
    at: datetime

