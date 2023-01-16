import asyncio
import logging

import motor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage
from aiogram_dialog import DialogRegistry

from tgbot.config import load_config
from tgbot.filters.role import RoleFilter, AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.dialogs.registration.dialogs import registration_dialog
from tgbot.handlers.user import register_user
from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.role import RoleMiddleware
from tgbot.repositories.fabric import create_repo_ad_sos_pg, create_repo_mock_services

logger = logging.getLogger(__name__)


async def create_mongo_connect_db(host, port, database_name: str = "work_db"):
    client = motor.motor_asyncio.AsyncIOMotorClient(host, port)
    await client.server_info()
    logger.info("CONNECT TO MONGO")
    db = client[database_name]

    return db


def register_all_dialogs(registry: DialogRegistry):
    registry.register(registration_dialog)


async def main():
    config = load_config()
    if config.tg_bot.use_redis:
        storage = RedisStorage()
    else:
        storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=storage)

    mongo_db = await create_mongo_connect_db(config.db.host, config.db.port)
    repo = create_repo_mock_services(mongo_db)
    bot['repo'] = repo
    dp.middleware.setup(RoleMiddleware(config.tg_bot.admin_ids, repo))
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)

    register_admin(dp)
    register_user(dp)
    registry = DialogRegistry(dp)
    register_all_dialogs(registry)

    # start
    try:
        logger.info("BOT STARTED")
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


def cli():
    """Wrapper for command line"""
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")


if __name__ == '__main__':
    cli()
