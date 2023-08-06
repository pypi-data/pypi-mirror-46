"""Base definition for Hockey clients."""

import logging
import time

import requests


class HockeyDerivedClient:
    """Base definition for Hockey clients.

    :param name: The name of the derived client
    :param token: The authentication token
    :param parent_logger: The parent logger that we will use for our own logging
    """

    log: logging.Logger
    token: str

    def __init__(self, name: str, token: str, parent_logger: logging.Logger) -> None:
        self.log = parent_logger.getChild(name)
        self.token = token

    def get(self, url: str, *, retry_count: int = 0) -> requests.Response:
        """Perform a GET request to a url

        :param url: The URL to run the GET on
        :param int retry_count: The number of retries remaining if we got a 202 last time

        :returns: The raw JSON response

        :raises Exception: If the request fails with a non 200 status code
        """
        response = requests.get(url, headers={"X-HockeyAppToken": self.token})

        if response.status_code == 202 and retry_count > 0:
            self.log.info(
                f"202 response. Sleeping for 10 seconds before invoking HockeyApp again..."
            )
            time.sleep(10)
            return self.get(url, retry_count=retry_count - 1)

        if response.status_code != 200:
            raise Exception(f"HockeyApp request failed: {url} Error: {response.text}")

        return response
