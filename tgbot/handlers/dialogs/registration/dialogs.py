from aiogram import types
from aiogram.dispatcher.filters import ContentTypeFilter
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from tgbot.handlers.dialogs.registration.handlers import start_reg, enter_phone
from tgbot.handlers.dialogs.registration.states import RegistrationSG

registration_dialog = Dialog(
    Window(
        Const('Бот для распределения вопросов.\n'
              'Сбор вопросов от рядовых сотрудников и их распределение'
              ' между Руководителями групп.'),
        Button(Const('Начало регистрации'), id='start_reg', on_click=start_reg),
        state=RegistrationSG.start
    ),
    Window(
        Const('Отправьте свой номер телефона'),
        MessageInput(enter_phone, content_types=types.ContentTypes.CONTACT),
        state=RegistrationSG.phone
    ),
    Window(
        Const('Ботом могут пользоваться только определенные сотрудники СТП'),
        state=RegistrationSG.error
    )
)
