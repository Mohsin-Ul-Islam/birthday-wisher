from os import environ
from typing import Protocol


class InvalidSecretReference(Exception):
    pass


class SecretManager(Protocol):
    def get(self, ref: str, version: str = "latest") -> str:
        raise NotImplementedError()


class Environment:
    def get(self, ref: str, _: str = "latest") -> str:

        secret = environ.get(ref)

        if secret is None:
            raise InvalidSecretReference(ref)

        return secret
