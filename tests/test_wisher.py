from datetime import datetime, timedelta
from typing import List

from expects import contain_exactly, equal, expect, have_length

from birthday_wisher import __version__
from birthday_wisher.user import User
from birthday_wisher.wisher import Wisher


class FakeNotifier:
    def __init__(self) -> None:
        self.messages: List[str] = []

    def notify(self, user: User, msg: str) -> None:
        self.messages.append(msg.format_map(user.asdict))


def users() -> List[User]:

    return [
        User(
            name="Mohsin Ul Islam",
            phone="+92123456789",
            email="test@mail.com",
            date_of_birth=datetime.now(),
        )
    ]


def test_version():
    expect(__version__).to(equal("1.0.1"))


def test_wisher_wishes_on_birthday() -> None:

    template = "Hello, {name}!"
    notifier = FakeNotifier()

    Wisher(template, users(), notifier).wish_all()

    expect(notifier.messages).to(have_length(1))
    expect(notifier.messages).to(contain_exactly("Hello, Mohsin Ul Islam!"))


def test_wisher_do_not_wishes_on_other_day() -> None:

    template = "Hello, {name}!"
    notifier = FakeNotifier()

    celebs = users()
    celebs[0].date_of_birth = datetime.now() + timedelta(days=1)

    Wisher(template, celebs, notifier).wish_all()
    expect(notifier.messages).to(have_length(0))
