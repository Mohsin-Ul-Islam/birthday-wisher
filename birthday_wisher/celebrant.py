from datetime import datetime
from typing import TypedDict


class Celebrant(TypedDict):
    name: str
    phone_number: str
    email: str
    date_of_birth: datetime
