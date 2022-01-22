from typing import Protocol

from twilio.rest import Client

from birthday_wisher.secrets import SecretManager
from birthday_wisher.user import User


class UserNotifier(Protocol):
    def notify(self, user: User, msg: str) -> None:
        raise NotImplementedError()


class TwilioSMSUserNotifier:
    def __init__(self, secrets: SecretManager) -> None:

        self.username = secrets.get("TWILIO_ACCOUNT_SID")
        self.password = secrets.get("TWILIO_AUTH_TOKEN")

        self.client = Client(self.username, self.password)
        self.phone = secrets.get("TWILIO_PHONE_NUMBER")

    def notify(self, user: User, msg: str) -> None:

        self.client.messages.create(
            from_=self.phone,
            to=user.phone,
            body=msg,
        )
