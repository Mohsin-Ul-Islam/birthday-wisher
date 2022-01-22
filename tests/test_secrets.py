from os import environ
from unittest.mock import Mock

from expects import equal, expect
from google.api_core.exceptions import NotFound
from pytest import raises

from birthday_wisher.secrets import (
    Environment,
    GoogleCloudSecretManager,
    InvalidSecretReference,
)


def test_environment_reads_from_env():

    environ["ABC"] = "abc"
    expect(Environment().get("ABC")).to(equal("abc"))


def test_environment_raises_exception_on_not_found():

    with raises(InvalidSecretReference, match="DEF"):
        Environment().get("DEF")


def test_google_secret_manager_get() -> None:

    client = Mock()
    client.secret_version_path = Mock(
        return_value="projects/aqua-gcloud/secrets/twilio-account-sid/latest"
    )
    client.access_secret_version = Mock()

    manager = GoogleCloudSecretManager(client)
    manager.get("TWILIO_ACCOUNT_SID")

    client.secret_version_path.assert_called_once_with(
        "aqua-gcloud", "twilio-account-sid", "latest"
    )
    client.access_secret_version.assert_called_once_with(
        request={
            "name": "projects/aqua-gcloud/secrets/twilio-account-sid/latest",
        }
    )


def test_google_secret_manager_get_raises() -> None:

    client = Mock()
    client.secret_version_path = Mock(
        return_value="projects/aqua-gcloud/secrets/twilio-account-sid/latest"
    )
    client.access_secret_version = Mock(side_effect=NotFound(""))

    manager = GoogleCloudSecretManager(client)

    with raises(InvalidSecretReference, match="TWILIO_ACCOUNT_SID"):
        manager.get("TWILIO_ACCOUNT_SID")
