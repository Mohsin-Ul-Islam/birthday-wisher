from os import environ

from expects import equal, expect
from pytest import raises

from birthday_wisher.secrets import Environment, InvalidSecretReference


def test_environment_reads_from_env():

    environ["ABC"] = "abc"
    expect(Environment().get("ABC")).to(equal("abc"))


def test_environment_raises_exception_on_not_found():

    with raises(InvalidSecretReference, match="DEF"):
        Environment().get("DEF")
