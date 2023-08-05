from typing import Union, Optional
from uuid import UUID

from datalogue.clients.http import _HttpClient, HttpMethod
from datalogue.models.organization import User, _user_from_payload, _users_from_payload
from datalogue.errors import DtlError


class _UserClient:
    """
    Client to interact with the User objects
    """

    def __init__(self, http_client: _HttpClient):
        self.http_client = http_client

    def get_current_user(self) -> Union[DtlError, User]:
        """
        Get information for current user

        :return: Error if it fails or user otherwise
        """
        res = self.http_client.make_authed_request("/user", HttpMethod.GET)

        if isinstance(res, DtlError):
            return DtlError("Could not retrieve user.", res)

        return _user_from_payload(res)

    def get(self, user_id: UUID) -> Union[DtlError, User]:
        """
        Get public user information: first_name, last_name, email
        for a given user_id .

        :param user_id: UUID
        :return: Error if it fails or user otherwise
        """

        params = {
            "id": str(user_id)
        }

        res = self.http_client.make_authed_request(f"/user/public", HttpMethod.GET, params=params)

        if isinstance(res, DtlError):
            return DtlError("Could not retreive user.", res)

        return _users_from_payload(res)
