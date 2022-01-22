from os import environ
from typing import Protocol

from google.api_core.exceptions import NotFound
from google.cloud.secretmanager import SecretManagerServiceClient


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


class GoogleCloudSecretManager:
    def __init__(
        self,
        client: SecretManagerServiceClient,
        project_id: str = "aqua-gcloud",
    ) -> None:
        self.client = client
        self.project_id = project_id

    def get(self, ref: str, version: str = "latest") -> str:

        try:
            return self.client.access_secret_version(
                request={
                    "name": self.client.secret_version_path(
                        self.project_id, ref.lower().replace("_", "-"), version
                    )
                }
            ).payload.data.decode("utf-8")

        except NotFound as err:
            raise InvalidSecretReference(ref) from err
