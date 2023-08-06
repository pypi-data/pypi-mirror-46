# Copyright 2018 PT Nodeflux Teknologi Indonesia.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
    nodeflux.cloud.auth.credentials
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implements the authentication credentials and several credentials loader.
"""

import os

from abc import ABC, abstractmethod
from typing import Tuple, Optional

import yaml

from nodeflux.cloud.utils import environment_vars as env
from nodeflux.cloud.utils.exceptions import NoCredentialsError


class Credentials:
    """Credentials for Nodeflux Cloud API authentication."""

    def __init__(
            self,
            api_key: str = None,
            secret_key: str = None,
            credentials_file_path: str = None,
    ):
        """Initialize a credentials

        The credentials could be loaded from several sources,
        with the following priorities:
            1. Explicit `api_key` and `secret_key` in the constructor
            2. Yaml file in `The `credentials_file_path`
            3. The `NODEFLUX_ACCESS_KEY` and `NODEFLUX_SECRET_KEY`
               environment variable
            4. Yaml file in `NODEFLUX_CREDENTIALS_FILE` environment variable

        Keyword Arguments:
            api_key {str} -- Nodeflux API key (default: {None})
            secret_key {str} -- Nodeflux API secret key (default: {None})
            credentials_file_path {str} -- Path to credentials yaml file
                                           (default: {None})

        Raises:
            NoCredentialsError -- Raised when no credentials are found.
        """

        if api_key and secret_key:
            self._api_key: Optional[str] = api_key
            self._secret_key: Optional[str] = secret_key

        else:
            loaders = [
                CredentialsFileLoader(credentials_file_path),
                EnvCredentialsLoader(),
                EnvCredentialsFileLoader(),
            ]

            for loader in loaders:
                self._api_key, self._secret_key = loader.load()

                if self._api_key and self._secret_key:
                    break
            else:
                raise NoCredentialsError

    @property
    def api_key(self):
        """Returns the API key."""
        return self._api_key

    @property
    def secret_key(self):
        """Returns the API secret key."""
        return self._secret_key


class CredentialsLoader(ABC):  # pylint:disable=too-few-public-methods
    """Abstract class for credentials loader."""

    @abstractmethod
    def load(self) -> Tuple[Optional[str], Optional[str]]:
        """Load credentials source and returns `(api_key, secret_key)`."""


class EnvCredentialsLoader(CredentialsLoader):  # pylint:disable=too-few-public-methods
    """Credential loader from environment variables.

    This loader will try to get the `api_key` and `secret_key` from the
    `NODEFLUX_ACCESS_KEY` and `NODEFLUX_SECRET_KEY` environment variable.
    """

    def load(self) -> Tuple[Optional[str], Optional[str]]:
        """Load credentials from environment variables."""
        api_key = os.environ.get(env.NODEFLUX_ACCESS_KEY, None)
        secret_key = os.environ.get(env.NODEFLUX_SECRET_KEY, None)

        return api_key, secret_key


class CredentialsFileLoader(CredentialsLoader):  # pylint:disable=too-few-public-methods
    """Credential loader from a file.

    This loader will try to get the `api_key` and `secret_key`
    from a yaml file.
    """

    def __init__(self, path: str = None) -> None:
        """Initialize loader from an explicit path."""
        self.path = path

    def load(self) -> Tuple[Optional[str], Optional[str]]:
        """Load credentials from a yaml file."""
        if self.path is None or not os.path.exists(self.path):
            return None, None

        with open(self.path, "r") as credentials_file:
            try:
                credentials = yaml.safe_load(credentials_file)

                return (credentials["api_key"], credentials["secret_key"])
            except yaml.YAMLError:
                return None, None


class EnvCredentialsFileLoader(CredentialsFileLoader):  # pylint:disable=too-few-public-methods
    """Credential loader from a file."""

    def __init__(self) -> None:
        """Initialize loader from environment variable."""
        super(EnvCredentialsFileLoader, self).__init__()
        self.path = os.environ.get(env.NODEFLUX_CREDENTIALS_FILE,
                                   "~/.nodeflux/credentials.yml")
