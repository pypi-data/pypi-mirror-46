"""Hockey versions API wrappers."""

import enum
import logging
import re
from typing import Dict, Iterator, List, Optional

import deserialize
import requests

import libhockey.constants
from libhockey.derived_client import HockeyDerivedClient


@deserialize.key("app_size", "appsize")
@deserialize.key("identifier", "id")
@deserialize.key("short_version", "shortversion")
class HockeyAppVersion:
    """Hockey API App Version."""

    app_id: int
    app_owner: str
    app_size: int
    block_crashes: bool
    config_url: str
    created_at: str
    device_family: Optional[str]
    download_url: Optional[str]
    expired_at: Optional[str]
    external: bool
    identifier: int
    mandatory: bool
    minimum_os_version: Optional[str]
    notes: str
    restricted_to_tags: bool
    sdk_version: Optional[str]
    short_version: str
    status: int
    timestamp: int
    title: str
    updated_at: str
    uuids: Optional[Dict[str, str]]
    version: str


class HockeyAppVersionsResponse:
    """Hockey API App Versions response."""

    app_versions: List[HockeyAppVersion]
    status: str
    current_page: int
    per_page: int
    total_entries: int
    total_pages: int


@deserialize.key("identifier", "id")
@deserialize.key("short_version", "shortversion")
class HockeyAppVersionStatistics:
    """Hockey API Statistics."""

    class Statistics:
        """The statistics struct from Hockey."""

        crashes: int
        devices: int
        downloads: int
        installs: int
        last_request_at: Optional[str]
        usage_time: str

    created_at: str
    identifier: int
    short_version: str
    statistics: Statistics
    version: str


@deserialize.key("app_size", "appsize")
@deserialize.key("identifier", "id")
@deserialize.key("short_version", "shortversion")
class HockeyUploadResponse:
    """Hockey upload API response."""

    app_size: Optional[int]
    block_crashes: bool
    block_personal_data: bool
    bundle_identifier: str
    company: str
    config_url: str
    created_at: str
    custom_release_type: str
    device_family: Optional[str]
    featured: bool
    identifier: int
    internal: bool
    minimum_os_version: Optional[str]
    notes: Optional[str]
    owner_token: str
    owner: str
    platform: str
    public_identifier: str
    public_url: str
    release_type: int
    retention_days: str
    role: int
    short_version: Optional[str]
    status: int
    timestamp: Optional[int]
    title: str
    updated_at: str
    version: Optional[str]
    visibility: str


class HockeyStatisticsResponse:
    """Hockey API statistics response."""

    app_versions: List[HockeyAppVersionStatistics]
    status: str


class HockeyVersionNotesType(enum.Enum):
    """Hockey notes types."""

    TEXTILE = 0
    MARKDOWN = 1


class HockeyUploadNotificationType(enum.Enum):
    """Hockey upload notification types."""

    DONT_NOTIFY = 0
    NOTIFY_ALL_INSTALLABLE = 1
    NOTIFY_ALL = 2


class HockeyUploadDownloadStatus(enum.Enum):
    """Hockey download status types."""

    DISALLOWED = 1
    AVAILABLE = 2


class HockeyUploadMandatory(enum.Enum):
    """Hockey mandatory types."""

    NO = 0
    YES = 1


class HockeyUploadReleaseType(enum.Enum):
    """Hockey release types."""

    ALPHA = 2
    BETA = 0
    STORE = 1
    ENTERPRISE = 3


class HockeyUploadRestrictionType(enum.Enum):
    """Hockey restriction types."""

    RESTRICTED = "7132"
    UNRESTRICTED = ""


class HockeyVersionsClient(HockeyDerivedClient):
    """Wrapper around the Hockey versions APIs.

    :param token: The authentication token
    :param parent_logger: The parent logger that we will use for our own logging
    """

    def __init__(self, token: str, parent_logger: logging.Logger) -> None:
        super().__init__("versions", token, parent_logger)

    def recent(self, app_id: str) -> List[HockeyAppVersion]:
        """Get the recent versions for the app ID.

        :param app_id: The ID of the app to get the versions for

        :returns: The list of versions found

        :raises Exception: If we fail to get the versions
        """

        self.log.info(f"Getting recent versions of app with id: {app_id}")

        request_url = f"{libhockey.constants.API_BASE_URL}/{app_id}?format=json"
        request_headers = {"X-HockeyAppToken": self.token}
        response = requests.get(request_url, headers=request_headers)

        if response.status_code != 200:
            raise Exception(
                f"Failed to get app versions: {response.status_code} -> {response.text}"
            )

        response_data: HockeyAppVersionsResponse = deserialize.deserialize(
            HockeyAppVersionsResponse, response.json()
        )

        return response_data.app_versions

    def generate_all(self, app_id: str, *, page: int = 1) -> Iterator[HockeyAppVersion]:
        """Get all app versions for the app ID.

        :param app_id: The ID for the app to get the versions for
        :param int page: The page of results to start at (leave unspecified for all)

        :returns: The list of app versions
        :rtype: HockeyAppVersion

        :raises Exception: If we don't get the app versions
        """

        request_url = f"{libhockey.constants.API_BASE_URL}/{app_id}/app_versions?page={page}"
        request_headers = {"X-HockeyAppToken": self.token}

        self.log.info(f"Fetching page {page} of app versions")
        response = requests.get(request_url, headers=request_headers)

        if response.status_code != 200:
            raise Exception(
                f"Failed to get app versions: {response.status_code} -> {response.text}"
            )

        response_data: HockeyAppVersionsResponse = deserialize.deserialize(
            HockeyAppVersionsResponse, response.json()
        )

        self.log.info(f"Fetched page {page}/{response_data.total_pages} of app versions")

        versions: List[HockeyAppVersion] = response_data.app_versions

        for version in versions:
            yield version

        if response_data.total_pages > page:
            yield from self.generate_all(app_id, page=page + 1)

    def all(self, app_id: str) -> List[HockeyAppVersion]:
        """Get all app versions for the app ID.

        :param app_id: The ID for the app to get the versions for

        :returns: The list of app versions

        :raises Exception: If we don't get the app versions
        """

        return list(self.generate_all(app_id))

    def hockey_version_identifier_for_version(self, app_id: str, version: str) -> Optional[int]:
        """Get the Hockey version identifier for the app version (usually build number).

        :param app_id: The ID for the app
        :param version: The app version (usually build number)

        :returns: The Hockey version identifier
        """

        for app_version in self.generate_all(app_id):
            if app_version.version == version:
                return app_version.identifier

        return None

    def latest_commit(self, app_id: str) -> Optional[str]:
        """Find the most recent release which has an available commit in it and return the commit hash.

        :param app_id: The ID of the app to get the versions for

        :returns: The latest commit available on Hockey
        """

        self.log.info(f"Getting latest commit for app: {app_id}")

        for version in self.generate_all(app_id):
            # Find commit sha in notes field
            matches = re.search("Commit: ([a-zA-Z0-9]+)", version.notes)

            if matches:
                version_match: str = matches.group(1).strip()
                return version_match

        return None

    def statistics(self, app_id: str) -> List[HockeyAppVersionStatistics]:
        """Get all version statistics for the app ID.

        :param app_id: The ID for the app to get the statistics for

        :returns: The list of app version statistics

        :raises Exception: If we don't get the statistics
        """

        request_url = f"{libhockey.constants.API_BASE_URL}/{app_id}/statistics"
        request_headers = {"X-HockeyAppToken": self.token}
        response = requests.get(request_url, headers=request_headers)

        if response.status_code != 200:
            raise Exception(
                f"Failed to get app versions: {response.status_code} -> {response.text}"
            )

        response_data: HockeyStatisticsResponse = deserialize.deserialize(
            HockeyStatisticsResponse, response.json()
        )

        return response_data.app_versions

    def upload(
        self,
        ipa_path: str,
        dsym_path: str,
        notes: str,
        release_type: HockeyUploadReleaseType,
        restriction_type: HockeyUploadRestrictionType,
        commit_sha: str,
    ) -> str:
        """Upload a new version of an app to Hockey.

        :param ipa_path: The path to the .ipa file to upload
        :param dsym_path: The path to the directory continaing the dSYM bundles
        :param notes: The release notes in Markdown format
        :param release_type: The type of release this is
        :param restriction_type: Whether this build should be restricted or not
        :param commit_sha: The commit that resulted in this build

        :returns: The URL to the build on Hockey

        :raises Exception: If we fail to upload the build
        :raises DeserializeException: If we fail to parse the upload response
        """

        # pylint: disable=too-many-locals

        ipa_file_name = ipa_path.split("/")[-1]
        dsym_file_name = dsym_path.split("/")[-1]

        self.log.info("IPA Name: " + ipa_file_name)
        self.log.info("dSYM Name: " + dsym_file_name)

        with open(ipa_path, "rb") as ipa_file:
            with open(dsym_path, "rb") as dsym_file:
                # Build request
                request_url = f"{libhockey.constants.API_BASE_URL}/upload"

                request_headers = {"X-HockeyAppToken": self.token}

                request_files = {
                    "ipa": (ipa_file_name, ipa_file),
                    "dsym": (dsym_file_name, dsym_file),
                }

                request_body = {
                    "notes": notes,
                    "notes_type": HockeyVersionNotesType.MARKDOWN.value,
                    "notify": HockeyUploadNotificationType.DONT_NOTIFY.value,
                    "status": HockeyUploadDownloadStatus.AVAILABLE.value,
                    "teams": restriction_type.value,
                    "mandatory": HockeyUploadMandatory.NO.value,
                    "release_type": release_type.value,
                    "commit_sha": commit_sha,
                    "retention_days": 28,
                }

                self.log.info("Hockey request: " + str(request_body))

                # Perform request
                response = requests.post(
                    request_url,
                    headers=request_headers,
                    files=request_files,
                    data=request_body,
                    timeout=20 * 60,
                )

        if response.status_code == 401:
            raise Exception("Invalid Hockeyapp token")

        if response.status_code != 201:
            raise Exception(
                f"Unsuccessful response status code: {response.status_code} -> {response.text.encode('utf-8')}"
            )

        # Print HockeyApp download link
        try:
            upload_response = deserialize.deserialize(HockeyUploadResponse, response.json())
        except deserialize.DeserializeException as ex:
            self.log.error(f"Failed to deserialize upload response: {ex}")
            raise

        version: str = upload_response.version
        if not version:
            # HockeyApp isn't current returning the `version` field.
            # In the current payload the version is only available in the config url.
            # This is a hack that we can hopefully remove once HockeyApp returns `version` again.
            #
            # Eg. https://rink.hockeyapp.net/manage/apps/208032/app_versions/57966
            self.log.warning(
                f"Failed to deserialize `version` from response, using config_url instead {response.json()}"
            )
            version = upload_response.config_url.split("/")[-1]

        return f"{upload_response.public_url}/app_versions/{version}"

        # pylint: enable=too-many-locals
