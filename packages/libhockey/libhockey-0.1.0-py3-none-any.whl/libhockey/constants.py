#!/usr/bin/env python3

"""Hockey API wrapper."""

import json
import logging
import re
import time
from typing import Any, ClassVar, Dict, List, Optional

import requests

from libhockey.crashes import HockeyCrashesClient
from libhockey.versions import HockeyVersionsClient


API_BASE_URL: str = "https://rink.hockeyapp.net/api/2/apps"


class HockeyClient:
    """Class responsible for getting data from HockeyApp through REST calls.

    :param str access_token: The access token to use for authentication. Leave as None to use KeyVault
    """

    log: logging.Logger
    token: str

    versions: HockeyVersionsClient
    crashes: HockeyCrashesClient

    def __init__(self, *, access_token: str) -> None:
        """Initialize the HockeyAppClient with the application id and the token."""

        self.log = logging.getLogger("libhockey")
        self.token = access_token
        self.crashes = HockeyCrashesClient(self.token, self.log)
        self.versions = HockeyVersionsClient(self.token, self.log)
