"""Interface to communicate with the external shop service."""
import json
from typing import Optional
import requests


class ExternalShop:
    """Class with base methods for the communication with the external shop service."""

    def __init__(self, ctx):
        self.ctx = ctx

    def service_base_url(self) -> str:
        """Return the base URL of the external shop service."""
        host = self.ctx.host.replace('https://', '').replace('http://', '')
        return 'https://{}/service/externalshop/'.format(host)

    def put_request(self, urlpath: str, data: dict) -> None:
        """Put a request to the external shop service."""
        url = self.service_base_url() + urlpath
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + self.ctx.auth_context.auth_token}
        ret = requests.put(url=url, headers=headers, data=json.dumps(data))
        if ret.status_code != 200:
            raise RuntimeError('Unable to put request ({}) Error: {} - {}'.format(url, ret.status_code, ret.text))

    def get_request(self, urlpath: str) -> Optional[dict]:
        """Send a GET request to the external shop service."""
        # noinspection PyBroadException
        try:
            url = self.service_base_url() + urlpath
            headers = {'Authorization': 'Bearer ' + self.ctx.auth_context.auth_token}
            ret = requests.get(url=url, headers=headers)
            if ret.status_code != 200:
                return None
            return ret.json()

        # pylint: disable=W0703
        except Exception:
            return None

    def get_request_field(self, urlpath: str, fieldname: str) -> Optional[str]:
        """Request the specified field from external shop service."""
        ret = self.get_request(urlpath)
        if not ret:
            return None
        return ret[fieldname]
