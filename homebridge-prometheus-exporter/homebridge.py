from os import access
import requests

from datetime import datetime


class HomeBridge:
    session = None
    token_expiry = None
    accessories = {}

    def __init__(self, url, username, password):

        self.username = username
        self.password = password
        self.url = url
        self.session = requests.Session()

    def _auth(self):
        now = datetime.now()
        if self.token_expiry is not None and self.token_expiry < now:
            return
        data = {
            "username": self.username,
            "password": self.password,
        }
        login_url = self.url + "/api/auth/login"
        response = requests.post(login_url, json=data)
        if response.status_code != 201:
            raise Exception(f"Failed to login with username {self.username}")
        result = response.json()
        self.token_expiry = now.timestamp() + (result["expires_in"] * 1000)
        self.session.headers["Authorization"] = f"Bearer {result['access_token']}"

    def get_accessories(self):
        self._auth()
        accessories_url = self.url + "/api/accessories"
        response = self.session.get(accessories_url)
        response.raise_for_status()
        return response.json()
