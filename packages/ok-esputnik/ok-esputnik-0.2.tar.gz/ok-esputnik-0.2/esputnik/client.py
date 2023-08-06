from functools import partial
from typing import Dict, Tuple, NamedTuple

import requests

from esputnik.exceptions import InvalidAuthDataError

__all__ = (
    'Response',
    'ESputnikAPIClient'
)


Response = NamedTuple('Response', [
    ('status_code', int),
    ('data', Dict)
])


class ESputnikAPIClient:
    """
    API client class that implements basic REST methods to talk with the
    server.

    Attributes:
        api_user (str): Unique API user passed on init.
        api_password (str): Unique API password passed on init.
    """

    def __init__(
            self,
            api_user: str,
            api_password: str,
            host: str,
            version: int = 1,
            *args,
            **kwargs
    ) -> None:
        self.api_user = api_user
        self.api_password = api_password
        if not self.api_user:
            raise InvalidAuthDataError(
                code='api_user',
                message='You must provide user.'
            )

        if not self.api_password:
            raise InvalidAuthDataError(
                code='api_password',
                message='You must provide password.'
            )

        self.host = host
        self.version = version

        super().__init__(*args, **kwargs)

    def __getattribute__(self, name: str):
        """
        Override default __getattribute__ to shorter request sending
        on remote server.
        For example instead of:
            >>>> object._send('get', 'url/path', data, headers)
        You can use:
            >>>> object.get('url/path', data, headers)

        Args:
            name (str): Property to get.
        """
        if name in ['get', 'post', 'put', 'delete']:
            return partial(self._send, name)
        return super().__getattribute__(name)

    def construct_url(self, *args) -> str:
        """
        Returns url with joined args as parts of url.

        Args:
            *args: part of url.

        Returns:
            str: URL
        """
        url = f'{self.host}v{self.version}/'

        if not args:
            return url

        joined_args = '/'.join([x.strip('/') for x in args]) + '/'

        return f'{url}{joined_args}'

    def get_auth_data(self) -> Tuple:
        return self.api_user, self.api_password

    @staticmethod
    def get_base_headers() -> Dict:
        return {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _send(
        self,
        method: str,
        path: str,
        data: Dict = None,
        headers: Dict = None,
        auth: Tuple = None
    ) -> Response:
        """
        Private method used to send request to the remote REST API server.

        Args:
            method (str): REST method to use.
            path (str): Corresponding relative path to send request.
            data (Dict, optional): Params to send.
            headers (Dict, optional): Request headers.
            auth (Tuple, optional): Auth data.

        Returns:
            Response: requests's response instance.

        Raises:
            AttributeError: Unsupported method was used.
        """
        url = self.construct_url(path)

        request_method = getattr(requests, method, None)

        if not request_method:
            raise AttributeError(f'{method} is not supported')

        if headers is None:
            headers = {}

        headers.update(self.get_base_headers())

        if auth is None:
            auth = self.get_auth_data()

        # Delete method accepts only path, without extra params
        if method == 'delete':
            response = request_method(
                url=url, headers=headers, auth=auth)
        else:
            response = request_method(
                url, data, headers=headers, auth=auth)

        return Response(
            status_code=response.status_code,
            data=response.json()
        )
