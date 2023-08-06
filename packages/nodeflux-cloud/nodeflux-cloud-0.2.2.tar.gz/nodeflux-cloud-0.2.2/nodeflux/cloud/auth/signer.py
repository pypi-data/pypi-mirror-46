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
    nodeflux.cloud.auth.signer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implements the authentication signer.
"""
# pylint: disable=no-self-use

from abc import ABC, abstractmethod
from typing import Dict
from hashlib import sha256

import hmac

from nodeflux.cloud.auth.credentials import Credentials


class Request:  # pylint:disable=too-few-public-methods
    """Request metadata to be signed"""

    def __init__(self, method: str, path: str, headers: Dict[str, str]) -> None:
        self.method = method
        self.path = path
        self.headers = headers


class BaseSigner(ABC):  # pylint:disable=too-few-public-methods
    """Base class for authentication signer."""

    @abstractmethod
    def token(self, request: Request) -> str:
        """Create a signed token from a request metadata."""


class AuthSignerV1(BaseSigner):
    """Nodeflux Authentication Signer V1

    This signer is designed based on AWS' Signature V4.
    """

    def __init__(self, credentials: Credentials) -> None:
        self.credentials = credentials

    def token(self, request: Request) -> str:
        canonical_request = self.canonical_request(request)
        string_to_sign = self.string_to_sign(request, canonical_request)
        signature = self.signature(string_to_sign, request)

        raw_token = [
            "NODEFLUX-HMAC-SHA256 "
            f"Credential={self.credentials.api_key}"
            f'/{request.headers["x-nodeflux-timestamp"][:8]}'
            f"{request.path}"
        ]
        raw_token.append(f"SignedHeaders={self.signed_headers(request.headers)}")
        raw_token.append(f"Signature={signature}")

        return ", ".join(raw_token)

    def canonical_request(self, request: Request) -> str:
        """Create a connonical version of the request metadata."""
        raw_cr = [request.method]
        raw_cr.append(request.path)
        raw_cr.append(self.canonical_headers(request.headers) + "\n")
        raw_cr.append(self.signed_headers(request.headers))

        return "\n".join(raw_cr)

    def canonical_headers(self, headers_to_sign: Dict[str, str]) -> str:
        """Return the headers that need to be included in the string_to_sign.

        The headers are returned in their canonical form by converting
        all header keys to lowercase, sorting them in alphabetical order,
        and joining them into a string, separated by newlines.
        """
        headers = []

        for key in sorted(headers_to_sign.keys()):
            value = self._header_value(headers_to_sign[key])
            headers.append(f"{key}:{value}")

        return "\n".join(headers)

    def _header_value(self, value):
        return " ".join(value.split())

    def string_to_sign(self, request: Request, canonical_request: str) -> str:
        """Return the canonical string to be signed."""
        headers = request.headers

        raw_string = ["NODEFLUX-HMAC-SHA256"]
        raw_string.append(headers["x-nodeflux-timestamp"])
        raw_string.append(f'{headers["x-nodeflux-timestamp"][:8]}{request.path}')
        raw_string.append(sha256(canonical_request.encode("utf-8")).hexdigest())

        return "\n".join(raw_string)

    def signed_headers(self, headers: Dict[str, str]) -> str:
        """Return the list of header key that has been signed.

        The keys are returned in their canonical form, sorted alphabetically,
        and joined into a string separated by `;`.
        """
        header_list = [f"{key.lower().strip()}" for key in headers.keys()]
        header_list = sorted(header_list)

        return ";".join(header_list)

    def signature(self, string_to_sign: str, request: Request) -> str:
        """Calculate the signature of a string and request metadata."""
        key = self.credentials.secret_key
        k_date = self._hmac_sign(
            ("Nodeflux" + key).encode("utf-8"),
            request.headers["x-nodeflux-timestamp"][:8],
        )
        k_path = self._hmac_sign(k_date, request.path)
        k_signing = self._hmac_sign(k_path, "NodefluxAuthV1")

        return self._hmac_sign_hex(k_signing, string_to_sign)

    def _hmac_sign(self, key: bytes, message: str) -> bytes:
        return hmac.new(key, message.encode("utf-8"), sha256).digest()

    def _hmac_sign_hex(self, key: bytes, message: str) -> str:
        return hmac.new(key, message.encode("utf-8"), sha256).hexdigest()
