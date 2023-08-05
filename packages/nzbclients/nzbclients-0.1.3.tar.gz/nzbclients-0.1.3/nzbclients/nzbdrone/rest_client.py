import logging
from typing import Dict, List, Union

import requests

logger = logging.getLogger(__name__)


class RestClient(object):
    default_headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def __init__(self, url: str, api_key: str, api_root: str = "api"):
        self._url = url
        self._api_key = api_key
        self._api_root = api_root

        self._session = requests.Session()

    def _delete(self, path: str, params: Dict = None) -> Union[List, Dict]:
        return self._send(method="DELETE", path=path, params=params)

    def _get(self, path: str, params: Dict = None) -> Union[List, Dict]:
        return self._send(method="GET", path=path, params=params)

    def _put(
        self, path: str, params: Dict = None, data: Dict = None
    ) -> Union[List, Dict]:
        return self._send(method="PUT", path=path, params=params, data=data)

    def _post(
        self, path: str, params: Dict = None, data: Dict = None
    ) -> Union[List, Dict]:
        return self._send(method="POST", path=path, params=params, data=data)

    def _send(
        self,
        method: str = "GET",
        path: str = "/",
        params: Dict = None,
        data: Dict = None,
    ) -> Union[List, Dict]:
        # Build our URL
        url = f"{self._url}/{self._api_root}{path}"

        # Update our params and add the API Key
        params = {} if params is None else params
        params.update({"apikey": self._api_key})

        response = self._session.request(
            method=method,
            url=url,
            params=params,
            json=data,
            headers=self.default_headers,
            timeout=60,
        )

        try:
            if response.text:
                response_content = response.json()
            else:
                response_content = response.content
        except ValueError:
            response_content = response.content

        if response.status_code == 200:
            logger.debug(
                "Received: {0}\n {1}".format(response.status_code, response_content)
            )
        elif response.status_code == 201:
            logger.debug(
                'Received: {0}\n "Created" response'.format(response.status_code)
            )
        elif response.status_code == 204:
            logger.debug(
                'Received: {0}\n "No Content" response'.format(response.status_code)
            )
        elif response.status_code == 401:
            logger.error(
                'Received: {0}\n "UNAUTHORIZED" response'.format(response.status_code)
            )
        elif response.status_code == 404:
            logger.error("Received: {0}\n Not Found".format(response.status_code))
        else:
            response.raise_for_status()

        return response_content
