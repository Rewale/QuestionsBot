from unittest.mock import AsyncMock

import pytest

from tgbot.handlers.dialogs.registration.handlers import enter_phone
from tgbot.handlers.dialogs.registration.states import RegistrationSG


@pytest.mark.asyncio
async def test_reg_wrong_phone():
    message_mock = AsyncMock()
    # Неверный номер телефона
    message_mock.text = "123123"
    dialog = AsyncMock()

    await enter_phone(message_mock, AsyncMock(), dialog)

    message_mock.reply.assert_called_with('Неверный формат номера телефона')
    dialog.switch_to.assert_called_with(RegistrationSG.phone)

