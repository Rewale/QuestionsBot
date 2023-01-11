import aiohttp

from tgbot.models.dto import User
from tgbot.models.role import UserRole
from tgbot.repositories import UserInfoRepo, JobTitleRepo


class ADUserInfo(UserInfoRepo):
    def __init__(self, url: str):
        self.url = url

    async def get_info(self, phone: str) -> User:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as resp:
                # сложная сериализация
                data = await resp.json()
                return User(**data)


class SSOJobTitleRoleRepo(JobTitleRepo):
    def __init__(self, url: str):
        self.url = url

    async def submit_job_title(self, job_title: str) -> UserRole:
        pass
