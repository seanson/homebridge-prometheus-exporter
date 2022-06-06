import requests
import logging

from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class HomeBridge:
    session = None
    token_expiry = datetime.fromtimestamp(0)
    accessories = {}

    def __init__(self, url, username, password):

        self.username = username
        self.password = password
        self.url = url
        self.session = requests.Session()

    def _auth(self):
        now = datetime.now()
        if now < self.token_expiry:
            logger.debug("Already logged in, %s <  %s", self.token_expiry, now)
            return
        data = {
            "username": self.username,
            "password": self.password,
        }
        logger.info("Auth token missing or expired, logging into HomeBridge")
        login_url = self.url + "/api/auth/login"
        response = requests.post(login_url, json=data)
        if response.status_code != 201:
            raise Exception(f"Failed to login with username {self.username}")
        result = response.json()
        self.token_expiry = now + timedelta(seconds=result["expires_in"])
        logger.info("New token_expiry: %s", self.token_expiry)
        self.session.headers.update(
            {"Authorization": f"Bearer {result['access_token']}"}
        )

    def get_accessories(self):
        self._auth()
        accessories_url = self.url + "/api/accessories"
        response = self.session.get(accessories_url)
        response.raise_for_status()
        return response.json()
