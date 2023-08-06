"""Hockey crashes API wrappers."""

import logging
from typing import Iterator, List, Optional

import deserialize

import libhockey.constants
from libhockey.derived_client import HockeyDerivedClient


@deserialize.key("identifier", "id")
@deserialize.key("crash_method", "method")
@deserialize.key("crash_file", "file")
@deserialize.key("crash_class", "class")
@deserialize.key("crash_line", "line")
class HockeyCrashGroup:
    """Represents a Hockey crash group."""

    identifier: int
    app_id: int
    created_at: str
    updated_at: str
    status: int
    reason: Optional[str]
    last_crash_at: str
    exception_type: Optional[str]
    fixed: bool
    app_version_id: int
    bundle_version: str
    bundle_short_version: str
    number_of_crashes: int
    grouping_hash: str
    grouping_type: int
    pattern: Optional[str]
    crash_method: Optional[str]
    crash_file: Optional[str]
    crash_class: Optional[str]
    crash_line: Optional[str]

    def url(self) -> str:
        """Return the access URL for the crash.

        :returns: The access URL
        """
        return f"https://rink.hockeyapp.net/manage/apps/{self.app_id}/app_versions/" + \
            f"{self.app_version_id}/crash_reasons/{self.identifier}"

    def __str__(self) -> str:
        """Generate and return the string representation of the object.

        :return: A string representation of the object
        """
        return str(
            {
                "Exception Type": self.exception_type,
                "Reason": self.reason,
                "Method": self.crash_method,
                "File": self.crash_file,
                "Class": self.crash_class,
                "Count": self.number_of_crashes,
            }
        )

    def __hash__(self) -> int:
        """Calculate the hash of the object

        :returns: The hash value of the object

        :raises Exception: If the language is not English
        """
        properties = [
            self.exception_type,
            self.reason,
            self.crash_method,
            self.crash_file,
            self.crash_class,
        ]

        return hash("-".join(map(str, properties)))

    def __eq__(self, other: object) -> bool:
        """Determine if the supplied object is equal to self

        :param other: The object to compare to self

        :returns: True if they are equal, False otherwise.
        """

        if not isinstance(other, HockeyCrashGroup):
            return False

        return self.__hash__() == other.__hash__()


class HockeyCrashGroupsResponse:
    """Represents a Hockey crash groups response."""

    crash_reasons: List[HockeyCrashGroup]
    status: str
    current_page: int
    per_page: int
    total_entries: int
    total_pages: int


@deserialize.key("identifier", "id")
class HockeyCrashInstance:
    """Represents a Hockey crash instance."""

    identifier: int
    app_id: int
    crash_reason_id: int
    created_at: str
    updated_at: str
    oem: str
    model: str
    os_version: str
    jail_break: bool
    contact_string: str
    user_string: str
    has_log: bool
    has_description: bool
    app_version_id: int
    bundle_version: str
    bundle_short_version: str


class HockeyCrashesResponse:
    """Represents a Hockey crashes response."""

    crash_reason: HockeyCrashGroup
    crashes: List[HockeyCrashInstance]
    status: str
    current_page: int
    per_page: int
    total_entries: int
    total_pages: int


class HockeyCrashesClient(HockeyDerivedClient):
    """Wrapper around the Hockey crashes APIs.

    :param token: The authentication token
    :param parent_logger: The parent logger that we will use for our own logging
    """

    def __init__(self, token: str, parent_logger: logging.Logger) -> None:
        super().__init__("crashes", token, parent_logger)

    def generate_groups_for_version(
        self, app_id: str, app_version_id: int, *, page: int = 1
    ) -> Iterator[HockeyCrashGroup]:
        """Get all crash groups for a given hockeyApp version.

        These crash groups are not guaranteed to be ordered in any particular way

        :param app_id: The ID of the app
        :param app_version_id: The version ID for the app
        :param int page: The page of crash groups to get

        :returns: The list of crash groups that were found
        :rtype: HockeyCrashGroup
        """

        request_url = f"{libhockey.constants.API_BASE_URL}/{app_id}/app_versions/{app_version_id}/" + \
            f"crash_reasons?per_page=100&order=desc&page={page}"

        self.log.info(f"Fetching page {page} of crash groups")

        response = self.get(request_url, retry_count=3)

        crash_reasons_response = deserialize.deserialize(HockeyCrashGroupsResponse, response.json())

        self.log.info(f"Fetched page {page}/{crash_reasons_response.total_pages} of crash groups")

        reasons: List[HockeyCrashGroup] = crash_reasons_response.crash_reasons

        for reason in reasons:
            yield reason

        if crash_reasons_response.total_pages > page:
            yield from self.generate_groups_for_version(app_id, app_version_id, page=page + 1)

    def groups_for_version(
        self, app_id: str, app_version_id: int, max_count: Optional[int] = None
    ) -> List[HockeyCrashGroup]:
        """Get all crash groups for a given hockeyApp version.

        :param app_id: The ID of the app
        :param app_version_id: The version ID for the app
        :param max_count: The maximum count of crash groups to fetch before stopping

        :returns: The list of crash groups that were found
        """

        groups = []

        for group in self.generate_groups_for_version(app_id, app_version_id):
            groups.append(group)

            if max_count is not None and len(groups) >= max_count:
                break

        return groups

    def generate_in_group(
        self, app_id: str, app_version_id: int, crash_group_id: int, *, page: int = 1
    ) -> Iterator[HockeyCrashInstance]:
        """Get all crash instances in a group.

        :param app_id: The ID of the app
        :param app_version_id: The version ID for the app
        :param crash_group_id: The ID of the group to get the crashes
        :param int page: The page of crashes to start at

        :returns: The crashes that were found in the group
        :rtype: HockeyCrashInstance
        """

        request_url = f"{libhockey.constants.API_BASE_URL}/{app_id}/app_versions/{app_version_id}/crash_reasons/" + \
            f"{crash_group_id}?per_page=100&order=desc&page={page}"
        response = self.get(request_url, retry_count=3)

        crashes_response = deserialize.deserialize(HockeyCrashesResponse, response.json())

        crashes: List[HockeyCrashInstance] = crashes_response.crashes

        for crash in crashes:
            yield crash

        if crashes_response.total_pages > page:
            yield from self.generate_in_group(app_id, app_version_id, crash_group_id, page=page + 1)

    def in_group(
        self, app_id: str, app_version_id: int, crash_group_id: int
    ) -> List[HockeyCrashInstance]:
        """Get all crash instances in a group.

        :param app_id: The ID of the app
        :param app_version_id: The version ID for the app
        :param crash_group_id: The ID of the group to get the crashes

        :returns: The list of crash instances that were found
        """

        return list(self.generate_in_group(app_id, app_version_id, crash_group_id))
