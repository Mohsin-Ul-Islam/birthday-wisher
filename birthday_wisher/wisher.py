from __future__ import annotations

from birthday_wisher.notifier import UserNotifier
from birthday_wisher.user import User


class Wisher:
    def __init__(
        self,
        template: str,
        users: list[User],
        notifier: UserNotifier,
    ) -> None:
        self.users = users
        self.notifier = notifier
        self.template = template

    def wish_all(self) -> None:

        for user in self._users_having_birthdays:
            self._wish_birthday_to(user)

    @property
    def _users_having_birthdays(self) -> list[User]:
        return [user for user in self.users if user.has_birthday]

    def _wish_birthday_to(self, user: User) -> None:
        self.notifier.notify(user, self.template.format_map(user.asdict))
