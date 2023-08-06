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
    nodeflux.cloud.transports.grpc_auth
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implements the authentication plugin for gRPC using the AuthSignerV1.
"""

import urllib
from datetime import datetime

import grpc

from nodeflux.cloud.auth.signer import AuthSignerV1, Request


class AuthMetadataPlugin(grpc.AuthMetadataPlugin):  # pylint: disable=too-few-public-methods
    """Custom authentication method for gRPC using Nodeflux AuthSignerV1."""

    def __init__(self, credentials):
        self._credentials = credentials
        self._signer = AuthSignerV1(credentials)

    def _get_authorization_headers(self, context):
        headers = {
            "x-nodeflux-timestamp": datetime.now().strftime("%Y%m%dT%H%M%SZ")
        }

        path = [urllib.parse.urlparse(context.service_url).path]
        path.append("/")
        path.append(context.method_name)

        request = Request("POST", "".join(path), headers)
        headers["authorization"] = self._signer.token(request)

        return list(headers.items())

    def __call__(self, context, callback):
        callback(self._get_authorization_headers(context), None)
