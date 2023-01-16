from aiogram import Dispatcher, types
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from tgbot.handlers.dialogs.registration.states import RegistrationSG


async def user_start(m: Message, dialog_manager: DialogManager):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Отправить номер телефона в бот", request_contact=True))
    await m.answer('Бот для распределения вопросов.\n'
                   'Сбор вопросов от рядовых сотрудников и их распределение'
                   ' между Руководителями групп.\n'
                   'Для начала использования необходимо пройти регистрацию', reply_markup=keyboard)
    await dialog_manager.start(RegistrationSG.phone, mode=StartMode.RESET_STACK)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*", role=None)
