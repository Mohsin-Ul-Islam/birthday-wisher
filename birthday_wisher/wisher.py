from __future__ import annotations

from datetime import date, timedelta
from typing import List

from birthday_wisher import Celebrant, Notifier


class Wisher:
    def __init__(
        self, celebrants: List[Celebrant], msg_format: str, notifier: Notifier
    ) -> None:
        self._celebrants = celebrants
        self._msg_format = msg_format
        self._notifier = notifier

    def wish_all(self) -> None:

        for celebrant in self._celebrants:
            if self._has_birthday_today(celebrant):
                self._notifier.notify(celebrant, self._msg_format)

    def _has_birthday_today(self, celebrant: Celebrant) -> bool:

        today = date.today() + timedelta(hours=9)
        birthdate = celebrant["date_of_birth"].date()

        return today.day == birthdate.day and today.month == birthdate.month
