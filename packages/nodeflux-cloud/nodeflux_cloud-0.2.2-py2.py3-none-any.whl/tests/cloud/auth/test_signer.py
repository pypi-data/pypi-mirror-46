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
    tests.cloud.auth.signer
    ~~~~~~~~~~~~~~~~~~~~~~~

    Test cases for the nodeflux.cloud.auth.signer module.
"""

# pylint: disable=no-self-use,redefined-outer-name

from datetime import datetime
from hashlib import sha256

import pytest

from nodeflux.cloud.auth.credentials import Credentials
from nodeflux.cloud.auth.signer import AuthSignerV1, Request


@pytest.fixture
def signer() -> AuthSignerV1:
    """Create a signer to be used in all tests."""
    credentials = Credentials("SOMEAPIKEY", "SOMESECRETKEY")

    return AuthSignerV1(credentials)


@pytest.fixture
def request_data() -> Request:
    """Create a request metadata to be used in all tests."""
    return Request(
        "POST",
        "/ImageAnalytic/BatchImageAnalytic",
        {
            "content-type": "application/grpc",
            "authority": "fire.nodeflux.io",
            "x-nodeflux-timestamp": datetime.now().strftime("%Y%m%dT%H%M%SZ"),
        },
    )


class TestAuthSignerV1:
    """Test cases for AuthSignerV1 class."""

    def test_canonical_request(self, signer: AuthSignerV1, request_data: Request):
        """Should produce a canonical form of the request."""
        canonical_request = signer.canonical_request(request_data)

        assert canonical_request == (
            "POST\n"
            "/ImageAnalytic/BatchImageAnalytic\n"
            "authority:fire.nodeflux.io\n"
            "content-type:application/grpc\n"
            f'x-nodeflux-timestamp:{request_data.headers["x-nodeflux-timestamp"]}\n'
            "\n"
            "authority;content-type;x-nodeflux-timestamp"
        )

    def test_string_to_sign(self, signer: AuthSignerV1, request_data: Request):
        """Should produce a string to be signed from the request metadata."""
        canonical_request = signer.canonical_request(request_data)
        string_to_sign = signer.string_to_sign(request_data, canonical_request)

        assert string_to_sign == (
            "NODEFLUX-HMAC-SHA256\n"
            f'{request_data.headers["x-nodeflux-timestamp"]}\n'
            f'{request_data.headers["x-nodeflux-timestamp"][:8]}'
            "/ImageAnalytic/BatchImageAnalytic\n"
            f'{sha256(canonical_request.encode("utf-8")).hexdigest()}'
        )

    def test_signature(self, signer: AuthSignerV1, request_data: Request):
        """Should produce a signature from the request metadata."""
        canonical_request = signer.canonical_request(request_data)
        string_to_sign = signer.string_to_sign(request_data, canonical_request)
        signature = signer.signature(string_to_sign, request_data)

        assert len(signature) == 64

    def test_token(self, signer: AuthSignerV1, request_data: Request):
        """Should produce an authorization token from the request metadata."""
        canonical_request = signer.canonical_request(request_data)
        string_to_sign = signer.string_to_sign(request_data, canonical_request)
        signature = signer.signature(string_to_sign, request_data)
        token = signer.token(request_data)

        splitted = token.split(", ")
        assert splitted[0] == (
            "NODEFLUX-HMAC-SHA256 "
            "Credential=SOMEAPIKEY/"
            f'{request_data.headers["x-nodeflux-timestamp"][:8]}'
            "/ImageAnalytic/BatchImageAnalytic"
        )

        assert splitted[1] == (
            "SignedHeaders=" "authority;content-type;x-nodeflux-timestamp"
        )

        assert splitted[2] == f"Signature={signature}"

    def test_compare_token(self, signer: AuthSignerV1, request_data: Request):
        """Two identical request metadata should produce an identical token."""
        token1 = signer.token(request_data)
        token2 = signer.token(request_data)

        assert token1 == token2
