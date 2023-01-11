import re

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Button

from tgbot.handlers.dialogs.registration.states import RegistrationSG
from tgbot.models.dto import User
from tgbot.repositories import Repo


async def start_reg(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(RegistrationSG.phone)


async def enter_phone(m: Message, proto, manager: DialogManager):
    phone = m.text
    if not re.match(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', phone):
        await m.reply("Неверный формат номера телефона")
        await manager.switch_to(RegistrationSG.phone)
        return
    repo: Repo = m.bot['repo']
    user_info = await repo.user_info.get_info(m.text)
    user_role = await repo.job_title.submit_job_title(user_info.job_title)
    if not user_role:
        await manager.switch_to(RegistrationSG.error)
        return
    user = User(**user_info.__dict__, telegram_id=m.from_user.id, role=user_role)
    await repo.user.create_user(user)
    await manager.done(user)
