import logging
import os

from httpx import Client
from utilities.logger_util import logger

class ApiClient(Client):
    def __init__(self, token=None):
        super().__init__(base_url=f"https://{os.getenv('API_HOST')}")
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