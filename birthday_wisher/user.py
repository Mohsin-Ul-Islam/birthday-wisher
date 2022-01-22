from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import TypedDict


class _UserDict(TypedDict):
    dob: str
    name: str
    email: str
    phone: str


@dataclass
class User:
    name: str
    phone: str
    email: str
    date_of_birth: datetime

    @property
    def has_birthday(self) -> bool:

        today = date.today() + timedelta(hours=9)
        birthdate = self.date_of_birth.date()

        return today.day == birthdate.day and today.month == birthdate.month

    @property
    def asdict(self) -> _UserDict:

        return _UserDict(
            name=self.name,
            email=self.email,
            phone=self.phone,
            dob=self.date_of_birth.isoformat(),
        )
