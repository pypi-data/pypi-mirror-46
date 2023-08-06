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
    tests.cloud.auth.credentials
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test cases for the nodeflux.cloud.auth.credentials module.
"""

# pylint: disable=no-self-use,redefined-outer-name

import os

import pytest
import yaml

from nodeflux.cloud.utils import environment_vars as env
from nodeflux.cloud.auth.credentials import Credentials


@pytest.fixture(scope="module")
def credential_file():
    """Create a credential file and remove it after the test is done."""
    credentials = {"api_key": "APIKEYFROMFILE", "secret_key": "SECRETKEYFROMFILE"}

    path = os.path.join(os.path.curdir, "credentials.yml")
    with open(path, "w") as creds:
        creds.write(yaml.dump(credentials))

    yield

    os.remove(path)


class TestCretentials:
    """Test cases for Credentials class and its loader."""

    def test_explicit_credentials(self):
        """Should use the given api key and secret key."""
        credentials = Credentials("SOMEAPIKEY", "SOMESECRETKEY")

        assert credentials.api_key == "SOMEAPIKEY"
        assert credentials.secret_key == "SOMESECRETKEY"

    def test_environment_credentials(self):
        """Should load the api key and secret key from environment variable."""
        os.environ[env.NODEFLUX_ACCESS_KEY] = "APIKEYFROMENV"
        os.environ[env.NODEFLUX_SECRET_KEY] = "SECRETKEYFROMENV"

        credentials = Credentials()

        assert credentials.api_key == "APIKEYFROMENV"
        assert credentials.secret_key == "SECRETKEYFROMENV"

        del os.environ[env.NODEFLUX_ACCESS_KEY]
        del os.environ[env.NODEFLUX_SECRET_KEY]

    def test_file_credentials(self, credential_file):  # pylint: disable=unused-argument
        """Should load the api key and secret key from a yaml file."""
        path = os.path.join(os.path.curdir, "credentials.yml")
        credentials = Credentials(credentials_file_path=path)

        assert credentials.api_key == "APIKEYFROMFILE"
        assert credentials.secret_key == "SECRETKEYFROMFILE"

    def test_file_env_credentials(
        self, credential_file
    ):  # pylint: disable=unused-argument
        """Should load the api key and secret key from a yaml file."""
        path = os.path.join(os.path.curdir, "credentials.yml")
        os.environ[env.NODEFLUX_CREDENTIALS_FILE] = path

        credentials = Credentials()

        assert credentials.api_key == "APIKEYFROMFILE"
        assert credentials.secret_key == "SECRETKEYFROMFILE"

    def test_loader_priority(self, credential_file):  # pylint: disable=unused-argument
        """Should use the keys env variable instead of the file env variable."""
        path = os.path.join(os.path.curdir, "credentials.yml")

        os.environ[env.NODEFLUX_ACCESS_KEY] = "APIKEYFROMENV"
        os.environ[env.NODEFLUX_SECRET_KEY] = "SECRETKEYFROMENV"
        os.environ[env.NODEFLUX_CREDENTIALS_FILE] = path

        credentials = Credentials()

        assert credentials.api_key == "APIKEYFROMENV"
        assert credentials.secret_key == "SECRETKEYFROMENV"
