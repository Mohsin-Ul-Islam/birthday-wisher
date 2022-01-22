from datetime import datetime, timedelta

from expects import be, equal, expect

from birthday_wisher.user import User


def user() -> User:

    return User(
        name="abc",
        phone="+921234567",
        email="abc@mail.com",
        date_of_birth=datetime.now(),
    )


def test_user_has_no_birthday() -> None:

    _user = user()
    _user.date_of_birth = datetime.now() + timedelta(days=1)
    expect(_user.has_birthday).to(be(False))


def test_user_has_birthday() -> None:

    _user = user()
    expect(_user.has_birthday).to(be(True))


def test_user_asdict() -> None:

    _user = user()

    actual = _user.asdict
    expected = dict(
        dob=_user.date_of_birth.isoformat(),
        name=_user.name,
        email=_user.email,
        phone=_user.phone,
    )

    expect(actual).to(equal(expected))
