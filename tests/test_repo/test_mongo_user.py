import asyncio
import copy

import motor
import pytest

from tgbot.models.dto import User
from tgbot.models.role import UserRole
from tgbot.repositories.mongo import UserMongoRepo


@pytest.fixture(scope='function')
def user_repo():
    client = motor.motor_asyncio.AsyncIOMotorClient()
    db = client.test_database
    yield UserMongoRepo(db, 'test_users')
    asyncio.get_event_loop().run_until_complete(db.workers.delete_many({}))
    client.close()


@pytest.mark.asyncio
async def test_insert(user_repo):
    input_user = User(name='Тест', surname='Тестовый', patronymic='Тестович', subdivision="123",
                      job_title="Младший специалист", role=UserRole.SPECIALIST, telegram_id=123123123)

    await user_repo.create_user(input_user)
    user = await user_repo.get_user(input_user.telegram_id)

    assert user.__dict__ == input_user.__dict__
