from tgbot.models.dto import UserInfo
from tgbot.models.role import UserRole
from tgbot.repositories import UserInfoRepo, JobTitleRepo


class ADUserInfoFake(UserInfoRepo):
    def __init__(self, url: str = ""):
        self.url = url

    async def get_info(self, phone: str) -> UserInfo:
        return UserInfo(name='Тест', patronymic='Тестович', surname='Тестовый', job_title='Сотрудник тех. поддержки',
                        subdivision='123')


class SSOJobTitleRoleRepoFake(JobTitleRepo):
    def __init__(self, url: str = ""):
        self.url = url

    async def submit_job_title(self, job_title: str) -> UserRole:
        return UserRole.SPECIALIST
