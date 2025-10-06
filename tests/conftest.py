import pytest
from dotenv import find_dotenv, load_dotenv


@pytest.fixture(scope="session", autouse=True)
def load_env() -> None:
    env_file = find_dotenv(".env.tests")
    load_dotenv(env_file)


def pytest_configure():
    env_file = find_dotenv(".env.tests")
    load_dotenv(env_file)
