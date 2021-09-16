from datetime import datetime, timedelta
from typing import List
from unittest import TestCase, main

from birthday_wisher import Celebrant, Notifier, Wisher, __version__


class FakeNotifier(Notifier):
    def __init__(self) -> None:
        self.messages = []

    def notify(self, celebrant: Celebrant, msg_format: str) -> None:
        self.messages.append(msg_format.format_map(celebrant))


class TestBirthdayWisher(TestCase):
    def __celebrants(self) -> List[Celebrant]:

        return [
            {
                "name": "Mohsin Ul Islam",
                "phone_number": "+92123456789",
                "email": "test@mail.com",
                "date_of_birth": datetime.now(),
            }
        ]

    def test_version(self):
        assert __version__ == "1.0.0"

    def test_wisher_wishes_on_birthday(self) -> None:

        celebrants = self.__celebrants()
        template = "Hello, {name}!"
        notifier = FakeNotifier()

        Wisher(celebrants, template, notifier).wish_all()

        self.assertEqual(len(notifier.messages), 1)
        self.assertIn("Hello, Mohsin Ul Islam!", notifier.messages)

    def test_wisher_do_not_wishes_on_other_day(self) -> None:

        celebrants = self.__celebrants()
        template = "Hello, {name}!"
        notifier = FakeNotifier()

        celebrants[0]["date_of_birth"] = datetime.now() + timedelta(days=1)

        Wisher(celebrants, template, notifier).wish_all()

        self.assertEqual(len(notifier.messages), 0)


if __name__ == "__main__":
    main()
