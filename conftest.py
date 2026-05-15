import logging
import os

import pytest
from dotenv import load_dotenv

from api.api_client import ApiClient
from api.auth_api import AuthApi
from api.user_api import UserApi
from tests.helpers import call_api, extract_access_token, extract_account_id
from utilities.logger_util import logger


def pytest_configure(config):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    load_dotenv(dotenv_path=".env")

    path = "logs/"
    os.makedirs(path, exist_ok=True)

    file_handler = logging.FileHandler(path + "api_test.log", "w")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter("%(lineno)d: %(asctime)s %(message)s"))

    custom_logger = logging.getLogger("custom_logger")
    custom_logger.setLevel(logging.INFO)
    custom_logger.addHandler(file_handler)


def pytest_runtest_setup(item):
    logger.info(f"{item.name}:")


@pytest.fixture
def api_client():
    return ApiClient()


@pytest.fixture
def auth_api(api_client):
    return AuthApi(api_client)


@pytest.fixture
def user_api(api_client):
    return UserApi(api_client)


@pytest.fixture
def user_credentials():
    username = os.getenv("USER_USERNAME")
    password = os.getenv("USER_PASSWORD")
    if not username or not password:
        pytest.skip("USER_USERNAME and USER_PASSWORD must be set in .env")
    return username, password


@pytest.fixture
def admin_credentials():
    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")
    if not username or not password:
        pytest.skip("ADMIN_USERNAME and ADMIN_PASSWORD must be set in .env")
    return username, password


@pytest.fixture
def moderator_credentials():
    username = os.getenv("MODERATOR_USERNAME")
    password = os.getenv("MODERATOR_PASSWORD")
    if not username or not password:
        pytest.skip("MODERATOR_USERNAME and MODERATOR_PASSWORD must be set in .env")
    return username, password


@pytest.fixture
def role_credentials(request):
    role, username_env, password_env = request.param
    username = os.getenv(username_env)
    password = os.getenv(password_env)

    if not username or not password:
        pytest.skip(f"{username_env} and {password_env} must be set in .env")

    return {
        "role": role,
        "username": username,
        "password": password,
    }


@pytest.fixture
def account_id_provider(api_client, auth_api, user_api):
    def get_account_id(credentials):
        username, password = credentials
        login_response = call_api("login before account id lookup", auth_api.login, username, password)
        token = extract_access_token(login_response)

        api_client.set_token(token)
        profile_response = call_api("get own profile before account id lookup", user_api.get_my_profile)

        return extract_account_id(profile_response)

    return get_account_id
