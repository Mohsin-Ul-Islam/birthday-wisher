from datetime import datetime
from unittest.mock import Mock

from expects import equal, expect

from birthday_wisher.notifier import TwilioSMSUserNotifier
from birthday_wisher.user import User


class FakeSecretManager:
    def get(self, ref: str, _: str = "latest") -> str:
        return ref


def test_twilio_reads_from_secrets() -> None:

    notifier = TwilioSMSUserNotifier(FakeSecretManager())

    expect(notifier.phone).to(equal("TWILIO_PHONE_NUMBER"))
    expect(notifier.username).to(equal("TWILIO_ACCOUNT_SID"))
    expect(notifier.password).to(equal("TWILIO_AUTH_TOKEN"))


def test_twilio_notify_uses_correct_data() -> None:

    user = User(
        name="abc",
        email="abc@mail.com",
        phone="+921234567",
        date_of_birth=datetime.now(),
    )

    notifier = TwilioSMSUserNotifier(FakeSecretManager())
    notifier.client.messages.create = Mock()
    notifier.notify(user, "Hello Mock!")

    notifier.client.messages.create.assert_called_once_with(
        to=user.phone,
        body="Hello Mock!",
        from_="TWILIO_PHONE_NUMBER",
    )
