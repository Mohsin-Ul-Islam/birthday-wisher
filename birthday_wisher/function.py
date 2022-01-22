from __future__ import annotations

from flask import Request, Response
from google.cloud.datastore import Client

from birthday_wisher.notifier import TwilioSMSUserNotifier
from birthday_wisher.secrets import Environment
from birthday_wisher.user import User
from birthday_wisher.wisher import Wisher


def handler(request: Request) -> Response:

    if request.headers.get("User-Agent") is None:
        return Response(response="Forbidden", status=403)

    notifier = TwilioSMSUserNotifier(Environment())
    template = """
        Happy Birthday {name}!
        May you have many more.\nRegards: Mohsin Ul Islam
        """

    users = [
        User(
            name=user.name,
            email=user.email,
            phone=user.phone_number,
            date_of_birth=user.date_of_birth,
        )
        for user in Client().query(kind="user").fetch()
    ]

    Wisher(template, users, notifier).wish_all()
    return Response(response="OK", status=200)
