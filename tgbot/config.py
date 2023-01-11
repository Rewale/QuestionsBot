import os
from dataclasses import dataclass
from typing import List

from environs import Env


@dataclass
class DbConfig:
    host: str
    port: int


@dataclass
class TgBot:
    token: str
    admin_ids: List[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class NotificationConfig:
    time_at: str
    day_at: int


@dataclass
class EmailConfig:
    is_ssl: bool
    email_domains: List[str]
    host: str
    port: int
    login: str
    password: str
    sender_email: str
    protocol_smtp = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    # misc: Miscellaneous
    # notification: NotificationConfig
    # email: EmailConfig


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            port=env.int('DB_PORT')
        ),
    )
