from abc import ABC, abstractmethod
from os import environ

from twilio.rest import Client

from birthday_wisher import Celebrant


class Notifier(ABC):
    @abstractmethod
    def notify(self, celebrant: Celebrant, msg_format: str) -> None:
        raise NotImplementedError


class SMSNotifier(Notifier):
    def notify(self, celebrant: Celebrant, msg_format: str) -> None:

        twilio_username = environ.get("TWILIO_ACCOUNT_SID")
        twilio_password = environ.get("TWILIO_AUTH_TOKEN")
        twilio_phonenum = environ.get("TWILIO_PHONE_NUMBER")

        twilio_client = Client(twilio_username, twilio_password)

        twilio_client.messages.create(
            from_=twilio_phonenum,
            to=celebrant["phone_number"],
            body=msg_format.format_map(celebrant),
        )
