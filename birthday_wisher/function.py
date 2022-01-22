from __future__ import annotations

from functools import wraps

from flask import Request, Response
from google.cloud.datastore import Client
from google.cloud.secretmanager import SecretManagerServiceClient

from birthday_wisher import secrets
from birthday_wisher.notifier import TwilioSMSUserNotifier
from birthday_wisher.user import User
from birthday_wisher.wisher import Wisher


def handle_exceptions(callback):
    @wraps(callback)
    def wrapper(*args, **kwargs):

        try:
            return callback(*args, **kwargs)
        except secrets.InvalidSecretReference as err:
            return Response(status=404, response=f"Cannot find secret: {err}")

    return wrapper


@handle_exceptions
def handler(_: Request) -> Response:

    notifier = TwilioSMSUserNotifier(
        secrets.GoogleCloudSecretManager(SecretManagerServiceClient())
    )
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
