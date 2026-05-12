import os

from httpx import Client
from utilities.logger_util import logger


class ApiClient(Client):
    def __init__(self, token=None):
        base_url = os.getenv("BASE_URL")
        if not base_url:
            raise ValueError("BASE_URL environment variable is not set")
        if not base_url.startswith(("http://", "https://")):
            base_url = f"https://{base_url}"

        super().__init__(base_url=base_url)
        if token:
            self.set_token(token)

    def set_token(self, token):
        self.headers["Authorization"] = f"Bearer {token}"

    def clear_token(self):
        self.headers.pop("Authorization", None)

    def request(self, method, path, **kwargs):
        logger.info("%s %s", method.upper(), path)
        response = super().request(method, path, **kwargs)
        logger.info(
            "%s %s -> %s",
            method.upper(),
            path,
            response.status_code
        )

        return response
