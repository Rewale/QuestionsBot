from aiogram import Dispatcher
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from tgbot.handlers.dialogs.registration.states import RegistrationSG


async def user_start(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(RegistrationSG.start, mode=StartMode.RESET_STACK)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
