from typing import List

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from tgbot.models.role import UserRole
from tgbot.repositories import Repo


class RoleMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, admin_ids: List[int], repo: Repo):
        super().__init__()
        self.admin_ids = admin_ids
        self.repo = repo

    async def pre_process(self, obj, data, *args):
        if not getattr(obj, "from_user", None):
            data["role"] = None
        elif obj.from_user.id in self.admin_ids:
            data["role"] = UserRole.ADMIN
        else:
            user = await self.repo.user.get_user(obj.from_user.id)
            if user:
                data["role"] = user.role
            else:
                data["role"] = None

    async def post_process(self, obj, data, *args):
        del data["role"]
