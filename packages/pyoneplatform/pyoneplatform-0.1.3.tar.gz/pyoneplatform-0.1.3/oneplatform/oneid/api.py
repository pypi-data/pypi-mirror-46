# -*- coding: utf-8 -*-
import requests
from .__about__ import __version__


class OneIDApi(object):
    """OneIDApi provides interface for One ID API."""
    DEFAULT_API_ENDPOINT = "https://one.th"
    DEFAULT_TIMEOUT = 5

    def __init__(self, client_id, client_secret, ref_code, endpoint=DEFAULT_API_ENDPOINT, timeout=DEFAULT_TIMEOUT):
        self.endpoint = endpoint
        self.timeout = timeout
        self.headers = {
            "User-Agent": "oneplatform-sdk-python/{}".format(__version__),
            "Content-Type": "application/json"
        }
        self.client_id = client_id
        self.client_secret = client_secret
        self.ref_code = ref_code

    def login(self, username="", password=""):
        data = {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": username,
            "password": password,
        }
        response = self._post("/api/oauth/getpwd", data=data)
        self.__check_error(response)
        return response.json()

    def refresh_token(self, refresh_token):
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = self._post("/api/oauth/get_refresh_token", data=data)
        self.__check_error(response)
        return response.json()

    def verify_authorize_code(self, authorize_code, redirect_url=None):
        if authorize_code == "":
            raise Exception("valid authorize code required")
        if redirect_url is None:
            redirect_url = ""
        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_url": redirect_url,
            "code": authorize_code,
            "scope": "",
        }
        response = self._post("/oauth/token", data=data)
        self.__check_error(response)
        return response.json()

    def get_profile(self, access_token):
        if access_token == "":
            raise Exception("logged in token required")
        headers = self._set_authorize_header(access_token)
        response = self._get("/api/account", headers=headers)
        self.__check_error(response)
        return response.json()

    def get_login_link(self):
        return '{}/api/oauth/getcode?client_id={}&response_type={}&scope={}'.format(
            self.endpoint,
            self.client_id,
            "code",
            ""
        )

    def _get(self, path, headers=None, timeout=None):
        url = self.endpoint + path
        if headers is None:
            headers = {}
        headers.update(self.headers)
        response = requests.get(
            url,
            headers=headers,
            timeout=timeout,
            verify=False
        )
        self.__check_error(response)
        return response

    def _post(self, path, data=None, headers=None, timeout=None):
        url = self.endpoint + path
        if headers is None:
            headers = {}
        headers.update(self.headers)
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=timeout,
            verify=False
        )
        self.__check_error(response)
        return response

    @staticmethod
    def __check_error(response):
        if 200 <= response.status_code < 300:
            pass
        else:
            raise Exception("error({}): {}".format(response.status_code, response.json()["errorMessage"]))

    @staticmethod
    def _set_authorize_header(access_token):
        return {
            "Authorization": "Bearer {}".format(access_token),
        }
