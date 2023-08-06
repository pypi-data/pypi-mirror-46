import time

import requests
from .config import get_config, get_credentials


class Token:

    def __init__(self, access_token, expires_in, refresh_token, refresh_expires_in, token_type, scope):
        self._access_token = access_token
        self._expires_in = expires_in
        self._refresh_token = refresh_token
        self._refresh_expires_in = refresh_expires_in
        self._token_type = token_type
        self._scope = scope
        self._creation_time = time.time()

    @classmethod
    def of_json(cls, json_repr):
        return cls(json_repr['access_token'], json_repr['expires_in'], json_repr['refresh_token'],
                   json_repr['refresh_expires_in'], json_repr['token_type'], json_repr['scope'])

    def is_expired(self):
        return time.time() - self._creation_time > self._expires_in

    @property
    def access_token(self):
        return self._access_token


_token = None


def get_access_token():
    global _token
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    form_params = get_credentials()
    if not _token or _token.is_expired():
        resp = requests.post(_form_auth_url(), headers=headers, data=form_params)
        resp.raise_for_status()
        _token = Token.of_json(resp.json())

    return _token.access_token


def _form_auth_url():
    config = get_config()
    return f'https://{config["auth_host"]}/auth/realms/{config["realm"]}/protocol/openid-connect/token'
