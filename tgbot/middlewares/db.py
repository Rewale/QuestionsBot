from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from tgbot.repositories import Repo


class DbMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, repo: Repo):
        super().__init__()
        self.repo = repo

    async def pre_process(self, obj, data, *args):
        data["repo"] = Repo

    async def post_process(self, obj, data, *args):
        del data["repo"]
